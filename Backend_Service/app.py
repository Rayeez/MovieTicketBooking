# # pip3 install flask pymongo
# # python3 app.py

from flask import Flask, request, jsonify
from pymongo import MongoClient
import copy

app = Flask(__name__)
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['mydatabase']
collection = db['mycollection']


@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    if data:
        inserted = collection.insert_one(data)
        return jsonify({"message": "Document created successfully", "id": str(inserted.inserted_id)}), 201
    else:
        return jsonify({"error": "Invalid data format"}, 400)


@app.route('/get_all', methods=['GET'])
def get_all():
    param = request.args.get('request')  # 'movie' or 'theater'

    if param == 'movie':
        data = list(collection.find({"type": "movie"}))
    elif param == 'theater':
        data = list(collection.find({"type": "theater"}))
    else:
        return jsonify({"error": "Invalid parameter value, use 'movie' or 'theater'"}, 400)

    for doc in data:
        doc['_id'] = str(doc['_id'])

    return jsonify(data), 200


@app.route('/get', methods=['GET'])
def get_data():
    param = request.args.get('request')  # 'movie' or 'theater'
    name = request.args.get('name')    # movie or theater name

    if param == 'movie':
        movies = collection.find_one({"type": "movie"})
        if movies:
            for movie in movies.get('movies', []):
                if movie['name'] == name:
                    return jsonify(movie), 200

    elif param == 'theater':
        theaters = collection.find_one({"type": "theater"})
        if theaters:
            for theater in theaters.get('theaters', []):
                if theater['theaterName'] == name:
                    return jsonify(theater), 200
    return jsonify({"error": "Document not found"}, 404)


@app.route('/update_seats', methods=['PUT'])
def update_seats():
    data = request.get_json()
    theater_name = data.get('theaterName')
    movie_name = data.get('movieName')
    showtime = data.get('showtime')
    occupied_seats = data.get('occupiedSeats')
    validate_occupied_seats = [x for x in occupied_seats if 1 <= x <= 100]
    if len(validate_occupied_seats) != len(occupied_seats):
        return jsonify({"error": "Select Valid Seats"}), 400

    if not theater_name or not movie_name or not showtime or not occupied_seats:
        return jsonify({"error": "Invalid data format, missing fields"}), 400

    filter = {
        "type": "theater",
        "theaters.theaterName": theater_name
    }
    
    update = {
        "$set": {
            "theaters.$.movies.$[movie].showtimes." + showtime + ".occupiedSeats": occupied_seats
        }
    }

    array_filters = [
        {"movie.name": movie_name}
    ]

    result = collection.update_one(filter, update, array_filters=array_filters)

    if result.modified_count > 0:
        return jsonify({'message': 'Seats updated successfully'}) , 200
    else:
        error_message = 'Select Different Seats'
        if result.raw_result.get('writeErrors'):
            error_message = 'Update failed with write error: ' + result.raw_result['writeErrors'][0]['errmsg']
        return jsonify({'error': error_message}), 404

if __name__ == '__main__':
    app.run(debug=True)
