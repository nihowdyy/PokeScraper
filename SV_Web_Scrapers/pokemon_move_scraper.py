import requests
from bs4 import BeautifulSoup
import csv
import os
import time

# URL from Pokemon DB
url = 'https://pokemondb.net/move/all'
page = requests.get(url)

# Beautiful Soup to parse html content
soup = BeautifulSoup(page.content, "html.parser")

# Headers of the information we want
HEADERS = [
    'Name', 'Type', 'Category', 
    'Power', 'Accuracy', 'PP', 
    'Short-Effect', 'Full-Effect'
]

# Directory Path & File Paths
directory = 'CSV Files'
file_name = 'PokemonMoves.csv'
file_path = os.path.join(directory, file_name)

# If Directory does not exist, create it
if not os.path.exists(directory):
    os.makedirs(directory)

# Scraping Time :)
with open(file_path, 'w',
          newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(HEADERS)

    # Table and rows
    table = soup.find('table')
    rows = table.find_all('tr')
    
    for row in rows[1:]:
        cells = row.find_all('td')

        moveName = cells[0].text.strip()
        moveType = cells[1].text.strip()
        moveCategory = cells[2].find('img')
        if moveCategory:
            moveCategory = moveCategory['title']
        else:
            moveCategory = 'None'
        movePower = cells[3].text.strip()
        moveAccuracy = cells[4].text.strip()
        movePP = cells[5].text.strip()
        moveEffect = cells[6].text.strip()

        # Find the long effect
        link = cells[0].find('a')['href']

        request = requests.get('https://pokemondb.net' + link)
        soup = BeautifulSoup(request.content, "html.parser")

        span = soup.find_all("span", class_="igame scarlet")

        if span:
            print("Found row:")

            span = span[-1]
            row = span.find_parent("tr")
            td = row.find("td")
            moveLongEffect = td.text.strip()
        else:
            h2 = soup.find("h2", id="move-effects")

            div = h2.find_parent("div")
            p = div.find('p')
            moveLongEffect = p.text.strip()

        data_out = [ moveName, moveType, moveCategory, 
                     movePower, moveAccuracy, movePP, 
                     moveEffect, moveLongEffect ]
        writer.writerow(data_out)
        print(data_out)
        # Cooldown
        time.sleep(1)
