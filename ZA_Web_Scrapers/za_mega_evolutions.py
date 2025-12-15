# Mega Evolutions Scraper (All Mega Evolutions w/ Stats)
import requests
from bs4 import BeautifulSoup
import csv
import os
import time

# URL from Game8
url = 'https://game8.co/games/Pokemon-Legends-Z-A/archives/446193'
page = requests.get(url)

# Beautiful Soup to parse HTML content
soup = BeautifulSoup(page.content, "html.parser")

# Headers of the information we want
HEADERS = [
    'Name', 'Type', 'Pre-Mega Form', 'HP', 
    'Atk', 'Def', 'SpAtk', 'SpDef', 'Speed',
    'Total', 'Evolution Item',
]

# Directory Path & File Path
directory = 'CSV Files'
file_name = 'ZAMegaEvolutions.csv'
file_path = os.path.join(directory, file_name)

# If Directory does not exist, create it
if not os.path.exists(directory):
    os.makedirs(directory)

# Mega Evolutions Pokemon Info
with open (file_path, 'w',
           newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(HEADERS)
        
    # All tables we require for Mega Evolutions
    tables = soup.find_all('table')[2:3]
    print (tables)

print ("Everything working!")