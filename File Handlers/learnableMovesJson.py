import csv
import json
import os

# 1. Set the File Locations for CSV and JSON

# CSV File
csv_directory = 'CSV Files'
csv_file = 'LearnableMoves.csv'

# If Directory does not exist, create it
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)
csv_path = os.path.join(csv_directory, csv_file)

# JSON File
json_directory = 'JSON Files'
json_file = 'LearnableMoves.json'

# If Directory does not exist, create it
if not os.path.exists(json_directory):
    os.makedirs(json_directory)
json_path = os.path.join(json_directory, json_file)

# 2. Set Field Mappings
field_mapping = {
    'Name': 'pokemon_name',
    'Level-up Learnset': 'level_up_learnset',
    'TM Learnset': 'tm_learnset',
    'Egg Moves': 'egg_moves'
}

# 3. Read CSV and convert to list of dictionaries

# Function to remove empty strings from a list
def remove_empty_strings(seq):
    return [x for x in seq if x.strip() != ""]

data = []
with open(csv_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        filtered_row = {field_mapping[field]: row[field] for field in csv_reader.fieldnames}
        filtered_row['level_up_learnset'] = remove_empty_strings(filtered_row['level_up_learnset'].split(','))
        filtered_row['tm_learnset'] = remove_empty_strings(filtered_row['tm_learnset'].split(','))
        filtered_row['egg_moves'] = remove_empty_strings(filtered_row['egg_moves'].split(','))

        data.append(filtered_row)

# 4.  Convert the data into more comprehensible form
def transform_data(entry):
    return {
        "name": entry['pokemon_name'],
        "learnset": {
            "level_up": entry['level_up_learnset'],
            "tms": entry['tm_learnset'],
            "egg_moves": entry['egg_moves']
        },
    }

# Check for duplicated entries
seen_names = set()
deduplicated_data = []
for entry in data:
    transformed_entry = transform_data(entry)
    if transformed_entry["name"] not in seen_names:
        deduplicated_data.append(transformed_entry)
        seen_names.add(transformed_entry["name"])

# 5. Write the list of dictionaries to a JSON file
with open(json_path, 'w') as file:
    json.dump(deduplicated_data, file, indent=4)

print(f"CSV Data successfully converted into JSON and save to {json_path}")