# pip install beautifulsoup4
# pip install requests

import requests
from bs4 import BeautifulSoup

# Define the Wikipedia page URL
# DC
# wikipedia_url = 'https://en.wikipedia.org/wiki/DC_Extended_Universe'
# Marvel
wikipedia_url = 'https://en.wikipedia.org/wiki/List_of_Marvel_Cinematic_Universe_films'

# Send an HTTP GET request to the URL
response = requests.get(wikipedia_url)

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table with the movie names
# DC
# movie_table = soup.find('table', {'class': 'wikitable plainrowheaders'})

# Marvel
movie_table = soup.find('table', {'class': 'wikitable plainrowheaders defaultcenter col2left'})

# Initialize lists to store movie names and image URLs
movie_names = []
image_urls = []
if movie_table:
# Loop through the rows of the table to extract data
    for row in movie_table.find_all('tr'):
        # Find the title link in each row
        title_cell = row.find('i')
        if title_cell:
            title_link = title_cell.find('a')
            if title_link:
                movie_name = title_link.get('title')
                movie_names.append(movie_name)

                # Open a new page for the movie link
                movie_url = title_link.get('href')
                movie_page = requests.get('https://en.wikipedia.org' + movie_url)
                movie_soup = BeautifulSoup(movie_page.text, 'html.parser')

                # Find the infobox for the movie
                infobox = movie_soup.find('table', {'class': 'infobox vevent'})

                # Find the image in the infobox
                img_tag = infobox.find('img')
                if img_tag:
                    image_url = img_tag.get('src')
                    image_urls.append(image_url)
                else:
                    image_urls.append(None)
            else:
                movie_names.append(None)
                image_urls.append(None)

# Print the extracted data
for i in range(len(movie_names)):
    print(f"Movie Name: {movie_names[i]}")
    print(f"Image URL: https:{image_urls[i]}")
    print()

# You can save this data to a file or use it as needed.
