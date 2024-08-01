import requests
import csv
import os
import time

# Open the CSV File
directory = 'CSV Files'
file_name = 'PKMN-SV-TMS.csv'
file_path = os.path.join(directory, file_name)
with open(file_path, 'r') as csvfile:
    # Reader Object
    csv_reader = csv.reader(csvfile)
    # Skip Header
    next(csv_reader, None)

    # Iterate for each row to pull the image file
    for row in csv_reader:
        # Pull Each Image in the file
        img_data = requests.get(row[7]).content

        # New Directories
        new_directory = 'TM Thumbnails'
        written_file_name = 'TM' + row[0] + ' ' + row[1] + '.jpg'
        file_path = os.path.join(new_directory, written_file_name)
        with open(file_path, 'wb') as handler:
            handler.write(img_data)
        
        # Go to Sleep
        time.sleep(1)

