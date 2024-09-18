import csv
import json
import os
import re

# 1. Set the File Locations for CSV and JSON

# CSV File
csv_directory = 'CSV Files'
csv_file = 'PKMN-SV-TMS.csv'

# If Directory does not exist, create it
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)
csv_path = os.path.join(csv_directory, csv_file)

# JSON File
json_directory = 'JSON Files'
json_file = 'PKMN-SV-TMS.json'

# If Directory does not exist, create it
if not os.path.exists(json_directory):
    os.makedirs(json_directory)
json_path = os.path.join(json_directory, json_file)

# 2. Set Field Mappings
field_mapping = {
    'TM Number': 'tm_number',
    'Name': 'tm_name',
    'Type': 'move_type',
    'Category': 'move_category',
    'Power': 'move_power',
    'Accuracy': 'move_accuracy',
    'PP': 'move_pp',
    'Location': 'tm_location',
    'LP Cost': 'tm_lp_cost',
    'Materials Needed': 'tm_materials',
    'Sell Price': 'tm_sell_price'
}


# 3. Read CSV and convert to list of dictionaries
included_fields = ['TM Number', 'Name', 'Type', 'Category', 
                   'Power', 'Accuracy', 'PP', 'Location', 
                   'LP Cost', 'Materials Needed', 'Sell Price']

data = []
with open(csv_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    filtered_data = []
    for row in csv_reader:
        filtered_row = {field_mapping[key]: row[key] for key in field_mapping if key in row}
        # TM Location Formatting
        filtered_row['tm_location'] = filtered_row['tm_location'].split(',')
        # TM Material Formatting
        material_entries = filtered_row['tm_materials'].split(',')

        # Define a list to store results
        materials = []
        for entry in material_entries:
            # User regex to find the material name and quantity
            match = re.match(r'(.+?) x(\d+)', entry.strip())
            if match:
                material_name = match.group(1).strip()
                pokemon_name = material_name.split(' ')[0]
                quantity = int(match.group(2))
                # Append the material as a dictionary to the list
                materials.append({
                    'material_name': material_name,
                    'pokemon_name': pokemon_name,
                    'quantity': quantity
                })
            filtered_row['tm_materials'] = materials
        data.append(filtered_row)

# 4.  Convert the data into more comprehensible form
def transform_data(entry):
    return {
        "tm_info": {
            "number": entry['tm_number'],
            'name': entry['tm_name'],
            'location': entry['tm_location'],
            'lp_cost': entry['tm_lp_cost'],
            'materials': entry['tm_materials'],
            'sell_price': entry['tm_sell_price']
        },
        'move_info': {
            'type': entry['move_type'],
            'category': entry['move_category'],
            'power': entry['move_power'],
            'accuracy': entry['move_accuracy'],
            'pp': entry['move_pp']
        }
    }
# Transform each entry in the list
transformed_data_list = [transform_data(entry) for entry in data]

# 5. Write the list of dictionaries to a JSON file
with open(json_path, 'w') as file:
    json.dump(transformed_data_list, file, indent=4)

print(f"CSV Data successfully converted into JSON and save to {json_path}")