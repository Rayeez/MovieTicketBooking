# Movie Theater Booking System - Flask API

This Flask API provides functionality for managing movie theater information, including creating documents, retrieving data, and updating seat availability.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Create Document](#create-document)
  - [Get All Documents](#get-all-documents)
  - [Get Document by Name](#get-document-by-name)
  - [Update Seat Availability](#update-seat-availability)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before using this Flask API, make sure you have the following prerequisites installed:

- Python 3
- Flask
- pymongo
- MongoDB

You can install Flask and pymongo using pip:

```bash
pip install flask pymongo
```

## Make sure MongoDB is installed and running locally on the default port (27017).

## Run the Flask API:

```
bash
python app.py
The API will start running at http://127.0.0.1:5000/ by default.
```

# Usage
## Create Document
To create a new document (movie or theater), send a POST request to the /create endpoint with a JSON request body. For example:

```
bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "Movie Name", "type": "movie", "showtimes": {...}}' http://127.0.0.1:5000/create
```

## Get All Documents
To retrieve all movies or theaters, send a GET request to the /get_all endpoint with a query parameter request set to either 'movie' or 'theater'. For example:
```
bash
curl http://127.0.0.1:5000/get_all?request=movie
```

## Get Document by Name
To retrieve a specific movie or theater by name, send a GET request to the /get endpoint with query parameters request (either 'movie' or 'theater') and name (the name of the movie or theater). For example:
```
bash
curl http://127.0.0.1:5000/get?request=movie&name=Movie Name
```

## Update Seat Availability
To update seat availability for a specific movie at a theater, send a PUT request to the /update_seats endpoint with a JSON request body containing theater name, movie name, showtime, and seat availability data. For example:

```
bash
curl -X PUT -H "Content-Type: application/json" -d '{"theaterName": "Theater Name", "movieName": "Movie Name", "showtime": "03:00 PM", "occupiedSeats": [1, 2, 3]}' http://127.0.0.1:5000/update_seats
```
Please ensure that the seat availability data contains only valid seat numbers (1 to 100).
