import requests
from bs4 import BeautifulSoup
import csv
import os
import time

# URL from Game8
url = 'https://game8.co/games/Pokemon-Scarlet-Violet/archives/369171'
page = requests.get(url)

# Beautiful Soup to parse html content
soup = BeautifulSoup(page.content, "html.parser")

# Headers of the Information we want
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

# Learnable Moves Info
with open(file_path, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(HEADERS)
        
    # All the tables that we want
    tables = soup.find_all('table')[1:5]
    
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('td')
            name = cells[0].text.strip()
            print(name)
            link = cells[0].findAll('a')[0]['href']

            # Find the individual moves by the links
            request = requests.get(link)
            soup = BeautifulSoup(request.content, "html.parser")
            
            # Level-up Learnset
            header = soup.find('h3', string='Learnset by Leveling Up')

            if header:
                table = header.find_next('table')
                if table:
                    print('Table Found:')
                    # Iterate through the rows
                    rows = table.find_all('tr')

                    # Learnset String
                    levelUp = ""

                    for row in rows[1::2]:
                        cells = row.find_all('td')
                        if (len(cells) == 1):
                            continue
                        # Move Information
                        level = cells[0].text.strip()
                        move = cells[1].find('a').text.strip()
                        
                        levelUp += f"{level}: {move},"
                else:
                    print("No table found after the header")
            else:
                print("Header not Found")

            # TM Learnset
            header = soup.find('h3', string="Learnset by TM")

            if header:
                table = header.find_next('table')
                if table:
                    print('Table Found:')
                    # Iterate through the rows
                    rows = table.find_all('tr')

                    # Learnset String
                    learnableTMs = ""

                    for row in rows[1::2]:
                        cells = row.find_all('td')
                        if (len(cells) == 1):
                            continue
                        # Move Information
                        move = cells[1].find('a').text.strip()
                        
                        learnableTMs += f"{move},"
                else:
                    print("No table found after the header")
            else:
                print("Header not Found")

            # Egg Moves
            header = soup.find('h3', string="Learnset via Egg Moves")

            if header:
                table = header.find_next('table')
                if table:
                    print('Table Found:')
                    # Iterate through the rows
                    rows = table.find_all('tr')

                    # Learnset String
                    eggMoves = ""

                    for row in rows[1::2]:
                        cells = row.find_all('td')
                        if (len(cells) == 1):
                            continue
                        # Move Information
                        move = cells[1].find('a').text.strip()
                        
                        eggMoves += f"{move},"
                else:
                    print("No table found after the header")
                    eggMoves = "N/A"
            else:
                print("Header not Found")

            if (eggMoves == ''):
                eggMoves = "No Egg Moves"
            data_out = [name, levelUp, learnableTMs, eggMoves]
            writer.writerow(data_out)

            print(data_out)

            # Cooldown
            time.sleep(1)


