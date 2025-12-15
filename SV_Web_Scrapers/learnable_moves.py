import requests
from bs4 import BeautifulSoup
import csv
import os
import time

# URL from Game8
url = 'https://game8.co/games/Pokemon-Scarlet-Violet/archives/369171'
page = requests.get(url)

# Beautiful Soup to parse HTML content
soup = BeautifulSoup(page.content, "html.parser")

# Headers of the information we want
HEADERS = [
    'Name', 'Level-up Learnset', 'TM Learnset', 'Egg Moves',
]

# Directory Path & File Path
directory = 'CSV Files'
file_name = 'LearnableMoves.csv'
file_path = os.path.join(directory, file_name)

# If Directory does not exist, create it
if not os.path.exists(directory):
    os.makedirs(directory)

# Last Processed Pokemon Name
def get_last_pokemon_name(csv_file):
    last_name = None
    if os.path.exists(csv_file):
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Skip the header row
            next(reader)
            # Iterate through the rows and store the last name
            for row in reader:
                last_name = row[0]  # Assuming the first column is the Pokémon name
    return last_name

# Helper function to extract learnset information
def get_learnset(soup, header_text):
    header = soup.find('h3', string=header_text)
    learnset = ""
    
    if header:
        table = header.find_next('table')
        if table:
            rows = table.find_all('tr')
            for row in rows[1::2]:  # Skip first row (header), then process each alternate row
                cells = row.find_all('td')
                if len(cells) == 1:
                    continue
                move = cells[1].find('a').text.strip() if cells[1].find('a') else cells[1].text.strip()
                if header_text == "Learnset by Leveling Up":
                    level = cells[0].text.strip()
                    learnset += f"{level} : {move},"
                else:
                    learnset += f"{move},"
        else:
            print(f"No table found for {header_text}")
    else:
        print(f"{header_text} not found")

    return learnset if learnset else "N/A"

# Learnable Moves Info & Tracker
last_processed = get_last_pokemon_name(file_path)
print(f"Last Processed Pokémon: {last_processed}")
last_processed_found = False

# Open the file for writing
with open(file_path, 'a', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    
    # Write headers only if the file is empty (i.e., no rows yet)
    if os.stat(file_path).st_size == 0:
        writer.writerow(HEADERS)
    
    # All the tables that we want
    tables = soup.find_all('table')[1:5]
    
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skipping the header row of the table
            cells = row.find_all('td')
            name = cells[0].text.strip()

            # Skip if this Pokémon has already been processed
            if name == last_processed:
                last_processed_found = True
                print(f"Skipping {name}, already processed.")
            elif last_processed_found:
                print(f"Processing {name}...")
                link = cells[0].findAll('a')[0]['href']

                # Find the individual moves by the links
                request = requests.get(link)
                soup = BeautifulSoup(request.content, "html.parser")
                
                # Level-up Learnset
                levelUp = get_learnset(soup, 'Learnset by Leveling Up')

                # TM Learnset
                learnableTMs = get_learnset(soup, "Learnset by TM")

                # Egg Moves
                eggMoves = get_learnset(soup, "Learnset via Egg Moves")
                if not eggMoves:
                    eggMoves = "No Egg Moves"

                # Output the data to CSV
                data_out = [name, levelUp, learnableTMs, eggMoves]
                writer.writerow(data_out)

                print(f"Processed {data_out}")
                # Cooldown
                time.sleep(1)
            else:
                print(f"Skipping {name}, already processed.")
