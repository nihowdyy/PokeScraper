# Pokemon Scarlet/Violet Item Scraper + Locations
import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import re

# Helper function to clean text chunks
def clean_chunk(s: str) -> str:
    s = s.strip(' "\t')
    s = s.replace("\r", " ").replace("\n", " ")
    s = re.sub(r"\s+", " ", s).strip()
    s = s.lstrip("•").strip()
    return s

# Function to scrape items and their locations
def scrape_items(url: str, file_path: str) -> None:
    # Headers of the information we want
    headers = ['Item Name', 'Effect', 'Location', 'Held By', 'Item Type']
    
    # Use a session (faster + more reliable than repeated plain requests)
    session = requests.Session()
    req_headers = {"User-Agent": "Mozilla/5.0"}

    page = session.get(url, headers=req_headers, timeout=30)
    page.raise_for_status()

    # Beautiful Soup to parse HTML content
    soup = BeautifulSoup(page.content, "html.parser")

    # Finding the main items table
    items_tables = soup.find_all('table')[0:4] # Only 4 tables with held items

    # Handling item types
    item_types = {
        1: 'In-Battle Items',
        2: 'Evolution Items',
        3: 'Overworld Items',
        4: 'Exp/EV Training Items'
    }

    # Open CSV file for writing
    with open(file_path, mode='w', newline='', encoding='utf-8') as outfile:
        # Creating CSV writer
        writer = csv.writer(outfile)
        writer.writerow(headers)

        # Iterating through each row in the items tables
        for table_index, table in enumerate(items_tables, start = 1):
            # Defining item type
            item_type = item_types.get(table_index, "Unknown")

            # Table rows
            rows = table.find_all('tr')
            # Iterating through each row to extract item data
            for row in rows[1:]: # Skip the header row
                # Finding all cells in the row
                cells = row.find_all('td')

                # Skips any weird rows
                if len(cells) < 2:
                    continue

                # Extracting item name
                item = cells[0].get_text(strip=True)
                # Extracting effect, locations, and held by information
                item_text = []
                for x in cells[1].stripped_strings:
                    cleaned = clean_chunk(x)
                    if cleaned:
                        item_text.append(cleaned)

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
                    location_parts = item_text[location_index:held_index]       
                    # Extracting held by information
                    held_chunks = item_text[held_index + 1:]
                    held_names = [x for x in held_chunks if x != "/"]
                    held_by = ", ".join(held_names) if held_names else "N/A"

                # Combining location parts
                location = ", ".join(location_parts) if location_parts else "N/A"

                # Writing data to CSV
                data_out = [item, effect, location, held_by, item_type]
                writer.writerow(data_out)

                # Confirmation print
                print (f"Written data for {item} to CSV.")

        # Final confirmation
        print ("Item scraping completed.")

if __name__ == "__main__":
    # URL from Game8
    url = "https://game8.co/games/Pokemon-Scarlet-Violet/archives/391045"

    # Directory Path & File Path
    directory = "CSV Files"
    file_name = "sv_items_and_locations.csv"
    file_path = os.path.join(directory, file_name)

    # If Directory does not exist, create it
    os.makedirs(directory, exist_ok=True)

    # Start scraping items
    scrape_items(url, file_path)
