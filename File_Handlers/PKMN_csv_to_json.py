import csv
import json
import os

# 1. Set the File Locations for CSV and JSON

# CSV File
csv_directory = 'CSV Files'
csv_file = 'PokedexSV.csv'

# If Directory does not exist, create it
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)
csv_path = os.path.join(csv_directory, csv_file)

# JSON File
json_directory = 'JSON Files'
json_file = 'PokedexSV.json'

# If Directory does not exist, create it
if not os.path.exists(json_directory):
    os.makedirs(json_directory)
json_path = os.path.join(json_directory, json_file)

# # 2. Set Field Mappings
field_mapping = {
    'Dex': 'dex_type',
    'No.': 'dex_number',
    'Name': 'pokemon_name',
    'Type': 'pokemon_type',
    'Abilities': 'pokemon_abilities',
    'Basic Stage': 'basic_stage',
    'HP': 'hp',
    'Atk': 'atk',
    'Def': 'def',
    'SpAtk': 'spatk',
    'SpDef': 'spdef',
    'Speed': 'speed',
    'Total': 'bst'
}

# 3. Read CSV and convert to list of dictionaries
data = []
with open(csv_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        filtered_row = {field_mapping[field]: row[field] for field in csv_reader.fieldnames}
        filtered_row['pokemon_type'] = filtered_row['pokemon_type'].split('&')
        filtered_row['pokemon_abilities'] = filtered_row['pokemon_abilities'].split('&')
        data.append(filtered_row)

# 4.  Convert the data into more comprehensible form
def transform_data(entry):
    return {
        "dex_info": {
            "type": entry["dex_type"],
            "number": entry["dex_number"]
        },
        "pokemon_info": {
            "name": entry["pokemon_name"],
            "type": entry["pokemon_type"],
            "abilities": entry["pokemon_abilities"],
            "basic_stage": entry["basic_stage"],
            "stats": {
                "hp": entry["hp"],
                "atk": entry["atk"],
                "def": entry["def"],
                "spatk": entry["spatk"],
                "spdef": entry["spdef"],
                "speed": entry["speed"],
                "bst": entry["bst"]
            }
        }
    }
# Transform each entry in the list
transformed_data_list = [transform_data(entry) for entry in data]

# 5. Write the list of dictionaries to a JSON file
with open(json_path, 'w') as file:
    json.dump(transformed_data_list, file, indent=4)

print(f"CSV Data successfully converted into JSON and save to {json_path}")