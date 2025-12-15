import requests
from bs4 import BeautifulSoup
import csv
import os

# The URL of serebii tm page
url = 'https://www.serebii.net/scarletviolet/tm.shtml'

# Make the GET request to fetch the raw HTML content
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <td> elements with class 'fooinfo' and colspan '6'
    td_elements = soup.find_all('td', class_='fooinfo', colspan='6')

    # Store the text content of every other matching <td> element in a list
    td_texts = [td.text.strip() for index, td in enumerate(td_elements) if index % 2 == 0]

    # Print the stored texts
    for text in td_texts:
        print(text)
    print(len(td_texts))

    # Directory Path & File Path
    directory = 'CSV Files'
    file_name = 'PKMN-SV-TMS.csv'
    file_path = os.path.join(directory, file_name)

    new_column_header = 'Description'  # Define your column header here

    # Read the existing data from the CSV file
    existing_data = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            existing_data = list(reader)  # Read the existing data into a list
    except FileNotFoundError:
        # If the file does not exist, we'll create it later
        existing_data = []

    # Check if there are existing rows
    if existing_data:
        # If the header does not already exist, add it
        if existing_data[0][0] != new_column_header:
            existing_data[0].append(new_column_header)  # Add header to first row

        # Fill the existing rows with the new data
        for i, text in enumerate(td_texts):
            if i < len(existing_data) - 1:  # Avoid index out of range
                existing_data[i + 1].append(text)  # Append to existing rows
            else:
                existing_data.append([''] + [text])  # Add new rows if necessary
    else:
        # If the file is empty, add the header and the new data
        existing_data.append([new_column_header])  # Start with a header row
        for text in td_texts:
            existing_data.append(['', text])  # Add each text in a new row under the header

    # Write the updated data back to the CSV file
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(existing_data)  # Write the updated data

    print(f"Successfully appended the list as a new column with header '{new_column_header}' to {file_path}.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


