# Pokemon Legends Z-A Learnable Moves Web Scraper
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import csv
import os
import time

# Lumiose Pokedex
# URL from Serebii
url_lumiose = 'https://www.serebii.net/legendsz-a/availablepokemon.shtml'
page_lumiose = requests.get(url_lumiose)

# Beautiful Soup to parse HTML content
soup_lumiose = BeautifulSoup(page_lumiose.content, "html.parser")

# Hyperspace Pokedex
url_hyperspace = 'https://www.serebii.net/legendsz-a/hyperspacepokedex.shtml'
page_hyperspace = requests.get(url_hyperspace)

# Beautiful Soup to parse HTML content
soup_hyperspace = BeautifulSoup(page_hyperspace.content, "html.parser")

# Headers of the information we want
HEADERS = [
    'Name', 'Level-Up Learnset', 'TM Learnset', 'Egg Moves',
]

# Directory Path & File Path
directory = 'CSV Files'
file_name = 'ZALearnableMoves.csv'
file_path = os.path.join (directory, file_name)

# If Directory does not exist, create it
if not os.path.exists(directory):
    os.makedirs(directory)

# Helper function to extract learnset information using anchor names
# Stantard Level Up: "standardlevel"
# TM/HM Moves: "tmhm"
def get_learnset(soup, anchor_name):
    # Looks for header with specific text, outputs "N/A" if not found
    anchor = soup.find('a', attrs={"name": anchor_name})
    if not anchor:
        print(f'Anchor "{anchor_name}" not found.')
        return "N/A"

    # Find the parent table, outputs "N/A" if not found
    table = anchor.find_parent('table')
    if not table:
        print(f"No parent table found for {anchor_name}.")
        return "N/A"

    # Find the header row within the table, outputs "N/A" if not found
    header_row = anchor.find_parent("tr")
    if not header_row:
        print(f"No header row (tr) found for {anchor_name}.")
        return "N/A"
    
    # Define blank learnset string for CSV output
    learnset = ""
    rows = table.find_all('tr')
    for row in rows [2::2]: # Skip first two rows (header), and column headings
        cells = row.find_all('td')

        # Skips any weird rows
        if len(cells) < 2:
            continue
        
        # Extract move name
        moves = cells[1].find('a').text.strip() if cells[1].find('a') else cells[1].text.strip()

        # Adds level info for level-up learnset, otherwise just move name
        if anchor_name == "standardlevel":
            level = next(cells[0].stripped_strings, "")
            learnset += f"{level} : {moves},"
        elif anchor_name == "tmhm":
            tm_num = cells[0].text.strip()
            learnset += f"{tm_num} : {moves},"
    
    return learnset if learnset else None

# Helper function to extract egg moves information
def get_egg_moves(soup, current_pokemon):
    # Extract egg moves from separate page
    egg_moves = ''
    href = soup.find('a', string='Egg Moves').get('href')
    egg_link = urljoin(current_pokemon, href)
    egg_page = requests.get(egg_link)
    egg_soup = BeautifulSoup(egg_page.content, "html.parser")

    # Extracting the tables and finding the egg moves within the tables
    tables = egg_soup.find_all('table', class_='dextable')

    # Extracting egg moves from the tables
    for table in tables[1:]:  # Skip first table with same class
        first_row = table.find('tr')
        cell = first_row.find('td')
        move = cell.get_text(strip=True)
        egg_moves += f"{move},"
    
    # Returns entire egg moveset
    return egg_moves if egg_moves else "No Egg Moves"

def scrape_pokedex_learnsets (soup, pokedex_header):
    # Main table with the Pokemon list
    table_header = soup.find('h2', string=pokedex_header)
    table = table_header.find_next ('table') 

    # Going through each Pokemon and extracting learnable moves
    rows = table.find_all('tr', recursive=False)
    for row in rows[1:]:
        cells = row.find_all('td', recursive=False)
        name = cells[2].find('a').get_text(strip=True)
        
        print (f"Processing {name}...")
        href = cells[2].find_all('a')[0]['href']
        current_pokemon = urljoin("https://www.serebii.net/", href)

        # Find individual moves by the links
        moves_page = requests.get(current_pokemon)
        moves_soup = BeautifulSoup(moves_page.content, "html.parser")

        # All Learnset extractions
        level_up = get_learnset(moves_soup, 'standardlevel')
        learnable_tm = get_learnset(moves_soup, 'tmhm')

        # Egg moves extraction
        egg_moves = get_egg_moves(moves_soup, current_pokemon)

        # Output the data to CSV
        data_out = [name, level_up, learnable_tm, egg_moves]
        writer.writerow(data_out)

        print (f"Written data for {name} to CSV.")

        # Cooldown to prevent overwhelming the server
        time.sleep(1)


# Open the file for writing
with open(file_path, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)

    # Write headers only if file is empty (i.e., no rows yet
    if os.stat(file_path).st_size == 0:
        writer.writerow(HEADERS)
    
    # Scraping Pokedexes from Pokemon Legends: Z-A
    scrape_pokedex_learnsets (soup_lumiose, 'List of Lumiose Pokédex in Pokémon Legends: Z-A')
    scrape_pokedex_learnsets (soup_hyperspace, 'List of Hyperspace Pokédex in Pokémon Legends: Z-A')

print ("Scraping of learnable moves completed!")

