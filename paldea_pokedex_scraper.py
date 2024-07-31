import requests
from bs4 import BeautifulSoup
import csv

# URL from Bulbapedia
url = 'https://game8.co/games/Pokemon-Scarlet-Violet/archives/369171'
page = requests.get(url)

# Beautiful Soup to parse html content
soup = BeautifulSoup(page.content, "html.parser")

# Second table being the content of the pokemon we want
table = soup.find_all('table')[1]

# Table Rows
rows = table.find_all('tr')

# Headers of the information we want
HEADERS = [
    'No.',
    'Name',
    'Image',
    'Type',
    'Abilities',
]

# Writing the csv file to store data to not need multiple calls
with open('SV_DEX.csv', 'w',
          newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(HEADERS)

    # Information to be stripped and to be written
    for row in rows[1:]:
        dex_num = row.find('th')
        number = dex_num.text.strip()

        cells = row.find_all('td')
        name = cells[0].text.strip()
        image = cells[0].findAll('img')[0]['data-src']

        text_pieces = [str(piece).strip() for piece in cells[1].stripped_strings]
        combined_text = '&'.join(text_pieces)
        type = combined_text

        text_pieces = [str(piece).strip() for piece in cells[2].stripped_strings]
        combined_text = '&'.join(text_pieces)
        abilities = combined_text

        data_out = [number, name, image, type, abilities]
        writer.writerow(data_out)