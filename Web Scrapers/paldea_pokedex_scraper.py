import requests
from bs4 import BeautifulSoup
import csv
import os

# URL from Bulbapedia
url = 'https://game8.co/games/Pokemon-Scarlet-Violet/archives/369171'
page = requests.get(url)

# Beautiful Soup to parse html content
soup = BeautifulSoup(page.content, "html.parser")

# Headers of the information we want
HEADERS = [
    'No.',
    'Name',
    'Image',
    'Type',
    'Abilities',
]

# Second table being the content of the pokemon we want (Paldea)
table = soup.find_all('table')[1]

# Table Rows
rows = table.find_all('tr')

# Directory Path & File Path
directory = 'CSV Files'
file_name = 'SV_DEX.csv'
file_path = os.path.join(directory, file_name)

# If Directory does not exist, create it
if not os.path.exists(directory):
    os.makedirs(directory)

# Paldean Pokedex Pokemon Info
with open(file_path, 'w',
          newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(HEADERS)

    # Information to be stripped and to be written
    for row in rows[1:]:
        dex_num = row.find('th')
        number = dex_num.text.strip()

        cells = row.find_all('td')
        # Remove Illegal characters
        name = cells[0].text.strip()
        name = name.replace('/', '&')
        image = cells[0].findAll('img')[0]['data-src']
        # Seperate the Pokemon Types
        text_pieces = [str(piece).strip() for piece in cells[1].stripped_strings]
        combined_text = '&'.join(text_pieces)
        type = combined_text
        # Seperate the Pokemon Abilities
        text_pieces = [str(piece).strip() for piece in cells[2].stripped_strings]
        combined_text = '&'.join(text_pieces)
        abilities = combined_text

        data_out = [number, name, image, type, abilities]
        writer.writerow(data_out)