# Pokemon Legends Z-A Learnable Moves Web Scraper
import requests
from bs4 import BeautifulSoup
import csv
import os
import time

# URL from Serebii
url = 'https://www.serebii.net/legendsz-a/availablepokemon.shtml'
page = requests.get(url)

# Beautiful Soup to parse HTML content
soup = BeautifulSoup(page.content, "html.parser")

# Headers of the information we want
HEADERS = [
    'Name', 'Level-up Learnset', 'TM Learnset', 'Egg Moves',
]

# Directory Path & File Path
directory = 'CSV Files'
file_name = 'ZALearnableMoves.csv'
file_path = os.path.join (directory, file_name)

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
    # Looks for header with specific text, outputs "N/A" if not found
    header = soup.find('h3', string=header_text)
    if not header:
        print (f"{header_text} not found.")
        return "N/A"

    # Find the parent table, outputs "N/A" if not found
    table = header.find_parent('table')
    if not table:
        print(f"No parent table found for {header_text}.")
        return "N/A"

    # Find the header row within the table, outputs "N/A" if not found
    header_row = header.find_parent("tr")
    if not header_row:
        print(f"No header row (tr) found for {header_text}.")
        return "N/A"
    
    

print ("Everything working!")