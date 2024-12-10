import csv
import json
import os

# 1. Set the File Locations for CSV and JSON

# CSV File
csv_directory = 'CSV Files'
csv_file = 'PokemonMoves.csv'

# If Directory does not exist, create it
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)
csv_path = os.path.join(csv_directory, csv_file)

# JSON File
json_directory = 'JSON Files'
json_file = 'PokemonMoves.json'

# If Directory does not exist, create it
if not os.path.exists(json_directory):
    os.makedirs(json_directory)
json_path = os.path.join(json_directory, json_file)

# 2. Set Field Mappings
field_mapping = {
    'Name': 'move_name',
    'Type': 'move_type',
    'Category': 'move_category',
    'Power': 'move_power',
    'Accuracy': 'move_accuracy',
    'PP': 'move_pp',
    'Short-Effect': 'move_short-effect',
    'Full-Effect': 'move_full-effect',
}

# 3. Read CSV and convert to list of dictionaries

# Function to remove empty strings from a list
def remove_empty_strings(seq):
    return [x for x in seq if x.strip() != ""]

data = []
with open(csv_path, mode='r', encoding='utf-8') as file:  # Specify UTF-8 encoding
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        # Map CSV fields to desired JSON fields
        filtered_row = {field_mapping[field]: row[field] for field in csv_reader.fieldnames if field in field_mapping}
        data.append(filtered_row)

# 4. Convert the data into a more comprehensible form
def transform_data(data):
    transformed = []
    for entry in data:
        transformed.append({
            "name": entry['move_name'],
            "move_details": {
                "type": entry['move_type'],
                "category": entry['move_category'],
                "power": entry['move_power'],
                "accuracy": entry['move_accuracy'],
                "pp": entry['move_pp'],
                "effect": {
                    "short": entry['move_short-effect'],
                    "full": entry['move_full-effect'],
                },
            },
        })
    return transformed

transformed_data = transform_data(data)

# 5. Write the list of dictionaries to a JSON file
with open(json_path, 'w', encoding='utf-8') as file:  # Ensure UTF-8 encoding for writing
    json.dump(transformed_data, file, indent=4, ensure_ascii=False)  # Allow non-ASCII characters

print(f"CSV Data successfully converted into JSON and saved to {json_path}")