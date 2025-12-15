import requests
from bs4 import BeautifulSoup
import csv
import os
import re

# URL from Bulbapedia
url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_TMs_in_Pok%C3%A9mon_Scarlet_and_Violet'
page = requests.get(url)

# Beautiful Soup to parse html content
soup = BeautifulSoup(page.content, "html.parser")

# First table being the content of the tms we want
table = soup.find_all('table')[0]

# Table Rows
rows = table.find_all('tr')

# Headers of the information we want
HEADERS = [
    'TM Number',
    'Name',
    'Type',
    'Category',
    'Power',
    'Accuracy',
    'PP',
    'IMAGE',
    'Location',
    'LP Cost',
    'Materials Needed',
    'Sell Price',
]

# Directory Path & File Path
directory = 'CSV Files'
file_name = 'PKMN-SV-TMS.csv'
file_path = os.path.join(directory, file_name)

# Writing the csv file to store data to not need multiple calls
with open(file_path, 'w',
          newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(HEADERS)

    # Information to be stripped and to be written
    count = 0
    for row in rows[2:]:
        count += 1
        cells = row.find_all('td')
        tm_number = str(count).zfill(3)
        move_name = cells[0].text.strip()
        move_type = cells[1].text.strip()
        move_category = cells[2].text.strip()
        move_power = str(int(cells[3].text.strip()[:3]))
        # Making the Move Power cells more nice looking
        if move_power == '0':
            move_power = 'None'
        move_accuracy = cells[4].text.strip()[:3]
        # Making the Move Accuracy cells more nice looking
        if move_accuracy == '—}}':
            move_accuracy = '0'
        move_accuracy = str(int(move_accuracy))
        if move_accuracy == '0':
            move_accuracy = 'Cannot Miss'
        move_pp = cells[5].text.strip()[:3]
        image = cells[6].findAll('img')[0]['src']

        # Clean up Location Information
        og_location = cells[7].text.strip()
        # Remove spaces after commas
        cleaned_location = re.sub(r',\s+', ',', og_location)
        # Add a comma before "Defeat Team"
        move_location = re.sub(r'Defeat Team', r',Defeat Team', cleaned_location)

        move_LP = cells[8].text.strip()
        # Clean up Material Information
        og_material = cells[9].text.strip()
        # Add a Comma between the Number and the Next Pokemon
        formatted_material = re.sub(r'(\d+)(?=\D)', r'\1,', og_material)
        formatted_material = re.sub(r'×', r'x', formatted_material)
        move_materials = formatted_material

        sell_price = cells[10].text.strip()
        data_out = [tm_number, move_name, move_type, move_category, move_power, move_accuracy, move_pp, image, move_location, move_LP, move_materials, sell_price]
        writer.writerow(data_out)



