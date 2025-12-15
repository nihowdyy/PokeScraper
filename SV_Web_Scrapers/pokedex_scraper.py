import requests
from bs4 import BeautifulSoup
import csv
import os
import time

# URL from Bulbapedia
url = 'https://game8.co/games/Pokemon-Scarlet-Violet/archives/369171'
page = requests.get(url)

# Beautiful Soup to parse html content
soup = BeautifulSoup(page.content, "html.parser")

# Headers of the information we want
HEADERS = [
    'Dex', 'No.', 'Name', 'Type', 'Abilities',
    'Basic Stage', 'HP', 'Atk', 'Def',
    'SpAtk', 'SpDef', 'Speed', 'Total',
]

# Directory Path & File Path
directory = 'CSV Files'
file_name = 'PokedexSV.csv'
file_path = os.path.join(directory, file_name)

# If Directory does not exist, create it
if not os.path.exists(directory):
    os.makedirs(directory)

# Paldean Pokedex Pokemon Info
with open(file_path, 'w',
          newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(HEADERS)

    # All the tables that we want
    tables = soup.find_all('table')[1:5]

    # Handling Dex Types
    dexes = {
        1: "Paldean",
        2: "National",
        3: "Kitakami",
        4: "Blueberry"
    }
    # Initializing count for Dex Types
    count = 0

    for table in tables:
        # Table Rows
        rows = table.find_all('tr')
        count += 1
        # Information to be stripped and to be written
        for row in rows[1:]:
            dex_element = row.find('th')
            # Formatting the Pokemon Dex Type
            dex_type = dexes.get(count)
            text_pieces = [str(piece).strip('_') for piece in dex_type]
            combined_text = ' '.join(text_pieces[0:1])
            dex_num = dex_element.text.strip()

            cells = row.find_all('td')
            name = cells[0].text.strip()

            # Seperate the Pokemon Types
            text_pieces = [str(piece).strip() for piece in cells[1].stripped_strings]
            combined_text = '&'.join(text_pieces)
            type = combined_text

            # Seperate the Pokemon Abilities
            text_pieces = [str(piece).strip() for piece in cells[2].stripped_strings]
            combined_text = '&'.join(text_pieces)
            abilities = combined_text
            
            # Stat Extraction
            total = cells[3].text.strip()
            hp = cells[4].text.strip()
            atk = cells[5].text.strip()
            defense = cells[6].text.strip()
            spatk = cells[7].text.strip()
            spdef = cells[8].text.strip()
            spd = cells[9].text.strip()

            # To track progress of the scraper
            print(f"Processing {dex_type} #{dex_num}: {name}")
            
            # Basic Stage
            link = cells[0].find_all('a')[0]['href']

            # Find the basic stage of the Pokemon
            request = requests.get(link)
            soup = BeautifulSoup(request.content, "html.parser")

            # See if the evolution table exists, if not, 
            # then it is already a basic pokemon
            target_table = None
            for table in soup.find_all('table'):
                headers = table.find_all('th')
                for header in headers:
                    if "Evolution Line" in header.get_text():
                        target_table = table
                        break
                if target_table:
                    break
            
            if (target_table == None):
                base = name
            # If it doesn't find the basic pokemon version.
            else:
                row = target_table.find_all('tr')
                cells = row[1].find_all('td')[0]
                if cells.find('b'):
                    base = cells.find('b').text.strip()
                elif cells.find('a'):
                    base = cells.find('a').text.strip()

            data_out = [dex_type, dex_num, name, type, abilities,
                        base, hp, atk, defense, spatk, spdef, spd, total]
            writer.writerow(data_out)
            
            # Cooldown to not overload servers
            time.sleep(1)

print ("Pokedex Scraping Complete!")
            