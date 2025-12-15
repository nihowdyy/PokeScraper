import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import time

# Scarlet Violet Dex (1)

# Open the CSV File
directory = 'CSV Files'
file_name = 'SV_DEX.csv'
file_path = os.path.join(directory, file_name)

# New Directories
new_directory = 'Pokemon Location images'

# If Directory does not exist, create it
if not os.path.exists(new_directory):
    os.makedirs(new_directory)

def image_downloader(file_path):
    with open(file_path, 'r') as csvfile:
        # Reader Object
        csv_reader = csv.reader(csvfile)
        # Skip Header
        next(csv_reader, None)

        # Iterate for each row to pull the image file
        for row in csv_reader:
            # Make a request for each pokemon
            page = requests.get(row[3])
            soup = BeautifulSoup(page.content, "html.parser")

            # Find all images
            images = soup.find_all('img', alt=re.compile("Location Map"))

            for image in images:
                image_src = image["data-src"]

                request = requests.get(image_src)
                img_data = request.content

                # New Directories
                written_file_name = image["alt"] + ".jpg"
                new_file_path = os.path.join(new_directory, written_file_name)
                with open(new_file_path, 'wb') as handler:
                    handler.write(img_data)
            time.sleep(1)

image_downloader(file_path)

# Teal Mask Dex (2)
file_name = 'TEAL_MASK_DEX.csv'
file_path = os.path.join(directory, file_name)

image_downloader(file_path)

# Indigo Disk Dex (3)
file_name = 'INDIGO_DISK_DEX.csv'
file_path = os.path.join(directory, file_name)

image_downloader(file_path)

# National Dex (4)
file_name = 'NAT_DEX.csv'
file_path = os.path.join(directory, file_name)

image_downloader(file_path)
