# Pokemon Scarlet/Violet Item Scraper + Locations
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import re

# URL from Game8
url = 'https://game8.co/games/Pokemon-Scarlet-Violet/archives/391045'
page = requests.get(url)

# Beautiful Soup to parse HTML content
soup = BeautifulSoup(page.content, "html.parser")

# Headers of the information we want
HEADERS = [
    'Item Name', 'Effect', 'Location', 'Held By', 'Item Type',
]

# Directory Path & File Path
directory = 'CSV Files'
file_name = 'sv_items_and_locations.csv'
file_path = os.path.join (directory, file_name)

# If Directory does not exist, create it
if not os.path.exists(directory):
    os.makedirs(directory)

# Helper function to clean text chunks
def clean_chunk(s: str) -> str:
    s = s.strip(' "\t')
    s = s.replace("\r", " ").replace("\n", " ")
    s = re.sub(r"\s+", " ", s).strip()
    s = s.lstrip("•").strip()
    return s

# Scraping items table from the website
# Open CSV file for writing
with open(file_path, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)

    # Write headers only if file is empty (i.e., no rows yet
    if os.stat(file_path).st_size == 0:
        writer.writerow(HEADERS)

    # Finding the main items table
    items_tables = soup.find_all('table')[0:4] # Only 4 tables with held items

    # Handling item types
    item_types = {
        1: 'In-Battle Items',
        2: 'Evolution Items',
        3: 'Overworld Items',
        4: 'Exp/EV Training Items'
    }

    # Initializing count for item types
    count = 0

    # Iterating through each row in the items tables
    for table in items_tables:
        # Table rows
        rows = table.find_all('tr')
        count += 1
        # Iterating through each row to extract item data
        for row in rows[1:]: # Skip the header row
            # Finding all cells in the row
            cells = row.find_all('td')
            item = cells[0].get_text(strip=True)

            # Extracting effect, locations, and held by information
            raw_chunks = list(cells[1].stripped_strings)
            item_text = [clean_chunk(x) for x in raw_chunks]
            item_text = [x for x in item_text if x]

            # Extracting effect
            effect = item_text[1] if len(item_text) > 1 else "N/A"

            # Finding held by index
            held_index = next(
                (i for i, s in enumerate(item_text) if s.lower().startswith("held item from")),
                None
            )

            # Defining location index
            location_index = 3

            # Extracting location and held by information
            if held_index is None: # No held by info
                location_parts = item_text[location_index:]
                held_by = "N/A"
            else: # Held by info exists
                # Extracting held by information
                location_parts = item_text[location_index:held_index]       
                held_chunks = item_text[held_index + 1:]
                held_names = [x for x in held_chunks if x != "/"]
                held_by = ", ".join(held_names) if held_names else "N/A"

            # Combining location parts
            location = ", ".join(location_parts) if location_parts else "N/A"

            # Writing data to CSV
            item_type = item_types.get(count)
            data_out = [item, effect, location, held_by, item_type]
            writer.writerow(data_out)

            # Confirmation print
            print (f"Written data for {item} to CSV.")

            # Cooldown to prevent overwhelming the server
            time.sleep(1)

    # Final confirmation
    print ("Item scraping completed.")

    