import requests
import csv
import os
import time

# Scarlet Violet Dex (1)

# Open the CSV File
directory = 'CSV Files'
file_name = 'SV_DEX.csv'
file_path = os.path.join(directory, file_name)
def image_downloader(file_path):
    with open(file_path, 'r') as csvfile:
        # Reader Object
        csv_reader = csv.reader(csvfile)
        # Skip Header
        next(csv_reader, None)

        # Iterate for each row to pull the image file
        for row in csv_reader:
            # Pull Each Image in the file
            request = requests.get(row[2])
            print(request)
            img_data = request.content
            
            # New Directories
            new_directory = 'Pokemon Images'
            written_file_name = row[1] + '.jpg'
            new_file_path = os.path.join(new_directory, written_file_name)
            with open(new_file_path, 'wb') as handler:
                handler.write(img_data)

            # Go to Sleep
            time.sleep(3)

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
