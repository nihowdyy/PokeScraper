# Pokemon Legends Z-A Learnable Moves Web Scraper
import requests
from bs4 import BeautifulSoup
import csv
import os
import time

# URL from Game8
url = 'https://game8.co/games/Pokemon-Legends-Z-A/archives/446180'
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

with open("pokedex.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print ("Everything working!")