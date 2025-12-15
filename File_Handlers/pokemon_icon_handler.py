# Import Modules
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image

# Finding IDs attached to the specific in-game icons and changing and formatting them
# to their corresponding National Dex Number + Pokemon Name

def id_handler():
    # Pokemon IDs for standard (Generation 5 and below)
    url = "https://www.serebii.net/pokemon/nationalpokedex.shtml"
    request = requests.get(url)

    # Beautiful Soup to parse html content
    soup = BeautifulSoup(request.content, "html.parser")

    # Table of National Dex
    table = soup.find('table', class_ = "dextable")

    # Rows of National Dex
    rows = table.find_all('tr')

    # Pull out all the ids 
    ids = {}
    for row in rows[2::2]:
        tds = row.find_all('td')
        id = str(int(tds[0].text.strip()[1:]))
        a = tds[3].find('a')
        value = a.text.strip()
        ids[id] = value
        if id == "649":
            break
    
    # Proper IDs by Pokemon:
    pids = {}
    for row in rows[2::2]:
        tds = row.find_all('td')
        id = tds[0].text.strip()[1:]
        a = tds[3].find('a')
        value = a.text.strip()
        pids[value] = id


    # Pokemon IDs for non-standard (Generation 6+)
    url = "https://www.vg-resource.com/thread-25872.html"
    request = requests.get(url)

    # Beautiful Soup to parse html content
    soup = BeautifulSoup(request.content, "html.parser")

    # Find all ids hidden in divs
    divs = soup.find_all('div', class_="spoiler_body")

    for div in divs:
        items = div.decode_contents().split('<br/>')

        for item in items:
            cleaned_item = item.strip()
            if cleaned_item:
                key, value = cleaned_item.split(' - ', 1)
                key = key.strip()
                value = value.strip()
                # Fix specific mispelt pokemon
                if key == '903':
                    value = "Chewtle"
                elif key == '922':
                    value = "Toxtricity"
                elif key == '934':
                    value = "Carkol"
                elif key == '969':
                    value = "Hatenna"
                elif key == '1032':
                    value = "Farigiraf"
                elif key == '1067':
                    value = "Nacli"
                ids[key] = value
    
    # Return Statement
    return ids, pids,

# Call ID Handler
ids, pids = id_handler()

# Directory Name
directory = 'Pokemon Icons'
    
# Iterate through files in directory
for name in os.listdir(directory):
    # Open File
    with open(os.path.join(directory, name)) as f:
        file_name = f'{name}'
    pokemon_id = str(int(file_name[2:6]))

    pokemon_name = ids.get(pokemon_id)

    # Regional Form Handler
    regional_num = file_name[10:12]
    
    regional_form = ""
    if (regional_num == '11'):
        regional_form = "Alolan"
    elif (regional_num == '31'):
        regional_form = "Galarian"
    elif (regional_num == '41'):
        regional_form = "Hisuian"
    elif (regional_num == '51'):
        regional_form = "Paldean"

    # Pokemon Form Handler:
    form_num = file_name[7:9]
    var_num = file_name[13:15]

    form_name = ""
    # Pikachu Forms
    if (pokemon_id == '25'):
        match form_num:
            case '11':
                form_name = "Original Cap"
            case '12':
                form_name = "Hoenn Cap"
            case '13':
                form_name = "Sinnoh Cap"
            case '14':
                form_name = "Unova Cap"
            case '15':
                form_name = "Kalos Cap"
            case '16':
                form_name = "Alola Cap"
            case '17':
                form_name = "Partner Cap"
            case '18':
                form_name = "World's Cap"
    # Tauros Forms
    elif (pokemon_id == '128'):
        match form_num:
            case '11': 
                form_name = "Combat Breed"
            case '12':
                form_name = "Blaze Breed"
            case '13':
                form_name = "Aqua Breed"
    # Deoxys Forms
    elif (pokemon_id == '386'):
        match form_num:
            case '11':
                form_name = "Normal Forme"
            case '12':
                    form_name = "Attack Forme"
            case '13':
                form_name = "Defense Forme"
            case '14':
                form_name = "Speed Forme"
    # Shellos Forms
    elif (pokemon_id == '422'):
        match form_num:
            case '11':
                form_name = "West Sea"
            case '12':
                form_name = "East Sea"
    # Gastrodon Forms
    elif (pokemon_id == '423'):
        match form_num:
            case '11':
                form_name = "West Sea"
            case '12':
                form_name = "East Sea"
    # Lumineon Forms
    elif (pokemon_id == '457'):
        match form_num:
            case '00':
                form_name = "Male"
            case '01':
                form_name = "Female"
    # Rotom Forms
    elif (pokemon_id == '479'):
        match form_num:
            case '12':
                form_name = "Heat"
            case '13':
                form_name = "Wash"
            case '14':
                form_name = "Frost"
            case '15':
                form_name = "Fan"
            case '16':
                form_name = "Mow"
    # Dialga Forms:
    elif (pokemon_id == '483'):
        match form_num:
            case '12':
                form_name = "Origin Forme"
    # Palkia Forms:
    elif (pokemon_id == '484'):
        match form_num:
            case '12':
                form_name = "Origin Forme"
    # Giratina Forms:
    elif (pokemon_id == '487'):
        match form_num:
            case '11':
                form_name = "Altered Forme"
            case '12':
                form_name = "Origin Forme"
    # Shaymin Forms:
    elif (pokemon_id == '492'):
        match form_num:
            case '11':
                form_name = "Land Forme"
            case '12':
                form_name = "Sky Forme"
    # Arceus Forms: 
    elif (pokemon_id == '493'):
        match var_num:
            case '01':
                form_name = "Fighting"
            case '02':
                form_name = "Flying"
            case '03':
                form_name = "Poison"
            case '04':
                form_name = "Ground"
            case '05':
                form_name = "Rock"
            case '06':
                form_name = "Bug"
            case '07':
                form_name = "Ghost"
            case '08':
                form_name = "Steel"
            case '09':
                form_name = "Fire"
            case '10':
                form_name = "Water"
            case '11':
                form_name = "Grass"
            case '12':
                form_name = "Electric"
            case '13':
                form_name = "Psychic"
            case '14':
                form_name = "Ice"
            case '15':
                form_name = "Dragon"
            case '16':
                form_name = "Dark"
            case '17':
                form_name = "Fairy"
    # Basculin Case
    elif (pokemon_id == '550'):
        match form_num:
            case '00':
                # Remove Hisuian for correctness
                regional_form = ""
                form_name = "White-Striped Form"
            case '11':
                form_name = "Red-Striped Form"
            case '12':
                form_name = "Blue-Striped Form"
    # Deerling Case
    elif (pokemon_id == '585'):
        match form_num:
            case '11':
                form_name = "Spring Form"
            case '12':
                form_name = "Summer Form"
            case '13':
                form_name = "Autumn Form"
            case '14':
                form_name = "Winter Form"
        # Sawsbuck Case
    elif (pokemon_id == '586'):
        match form_num:
            case '11':
                form_name = "Spring Form"
            case '12':
                form_name = "Summer Form"
            case '13':
                form_name = "Autumn Form"
            case '14':
                form_name = "Winter Form"
    # Tornadus Case
    elif (pokemon_id == '641'):
        match form_num:
            case '11':
                form_name = "Incarnate Forme"
            case '12':
                form_name = "Therian Forme"
    # Thundurus Case
    elif (pokemon_id == '642'):
        match form_num:
            case '11':
                form_name = "Incarnate Forme"
            case '12':
                form_name = "Therian Forme"
    # Landorus Case
    elif (pokemon_id == '645'):
        match form_num:
            case '11':
                form_name = "Incarnate Forme"
            case '12':
                form_name = "Therian Forme"
    # Kyurem Case
    elif (pokemon_id == '646'):
        match form_num:
            case '12':
                form_name = "White"
            case '13':
                form_name = "Black"
    # Keldeo Case
    elif (pokemon_id == '647'):
        match form_num:
            case '11':
                form_name = "Ordinary Form"
            case '12':
                form_name = "Resolute Form"
    # Meloetta Case
    elif (pokemon_id == '648'):
        match form_num:
            case '11':
                form_name = "Aria Forme"
            case '12':
                form_name = "Pirouette Forme"
    # Pyroar Case
    elif (pokemon_id == '705'):
        match form_num:
            case '00':
                form_name = "Male"
            case '01':
                form_name = "Female"
    # Vivillion Case
    elif (pokemon_id == '708'):
        match form_num:
            case '11':
                form_name = "Icy Snow"
            case '12':
                form_name = "Polar"
            case '13':
                form_name = "Tundra"
            case '14':
                form_name = "Continental"
            case '15':
                form_name = "Garden"
            case '16':
                form_name = "Elegant"
            case '17':
                form_name = "Meadow"
            case '18':
                form_name = "Modern"
            case '19':
                form_name = "Marine"
            case '20':
                form_name = "Archipelago"
            case '21':
                form_name = "High Plains"
            case '22':
                form_name = "Sandstorm"
            case '23':
                form_name = "River"
            case '24':
                form_name = "Monsoon"
            case '25':
                form_name = "Savanna"
            case '26':
                form_name = "Sun"
            case '27':
                form_name = "Ocean"
            case '28':
                form_name = "Jungle"
            case '29':
                form_name = "Fancy"
            case '30':
                form_name = "Poke Ball"
    # Floette Case
    elif (pokemon_id == '713'):
        match form_num:
            case '11':
                form_name = "Red Flower"
            case '12':
                form_name = "Yellow Flower"
            case '13':
                form_name = "Orange Flower"
            case '14':
                form_name = "Blue Flower"
            case '15':
                form_name = "White Flower"
    # Flabebe Case
    elif (pokemon_id == '714'):
        match form_num:
            case '11':
                form_name = "Red Flower"
            case '12':
                form_name = "Yellow Flower"
            case '13':
                form_name = "Orange Flower"
            case '14':
                form_name = "Blue Flower"
            case '15':
                form_name = "White Flower"
    # Florges Case
    elif (pokemon_id == '715'):
        match form_num:
            case '11':
                form_name = "Red Flower"
            case '12':
                form_name = "Yellow Flower"
            case '13':
                form_name = "Orange Flower"
            case '14':
                form_name = "Blue Flower"
            case '15':
                form_name = "White Flower"
    # Meowstic Case
    elif (pokemon_id == '734'):
        match form_num:
            case '00':
                form_name = "Male"
            case '01':
                form_name = "Female"
    # Hoopa Case
    elif (pokemon_id == '774'):
        match form_num:
            case '11':
                form_name = "Confined"
            case '12':
                form_name = "Unbound"
    # Minior Case:
    elif (pokemon_id == '824'):
        if form_num == '11':
            form_name = "Meteor Form"
        else:
            match var_num:
                case '00':
                    form_name = "Red Core"
                case '01':
                    form_name = "Orange Core"
                case '02':
                    form_name = "Yellow Core"
                case '03':
                    form_name = "Green Core"
                case '04':
                    form_name = "Blue Core"
                case '05':
                    form_name = "Indigo Core"
                case '06':
                    form_name = "Violet Core"
    # Oricorio Case:
    elif (pokemon_id == '825'):
        match form_num:
            case '11':
                form_name = "Baile Style"
            case '12':
                form_name = "Pom-Pom Style"
            case '13':
                form_name = "Pa'U Style"
            case '14':
                form_name = "Sensu Style"
    # Lycanroc Case:
    elif (pokemon_id == '829'):
        match form_num:
            case '11':
                form_name = "Midday Form"
            case '12':
                form_name = "Midnight Form"
            case '13':
                form_name = "Dusk Form"
    # Necrozma Case:
    elif (pokemon_id == '865'):
        match form_num:
            case '12':
                form_name = "Dusk Mane"
            case '13':
                form_name = "Dawn Wings"
    # Magearna Case
    elif (pokemon_id == '882'):
        match form_num:
            case '12':
                form_name = "Original Color"
    # Cramorant Case
    elif (pokemon_id == '917'):
        match form_num:
            case '12':
                form_name = "Gulping Form"
            case '13':
                form_name = "Gorging Form"
    # Toxtricitiy Case
    elif (pokemon_id == '922'):
        match form_num:
            case '11':
                form_name = "Amped Form"
            case '12':
                form_name = "Low Key Form"
    # Alcremie Case
    elif (pokemon_id == '925'):
        match form_num:
            case '11':
                form_name = "Vanilla Cream"
            case '12':
                form_name = "Ruby Cream"
            case '13':
                form_name = "Matcha Cream"
            case '14':
                form_name = "Mint Cream"
            case '15':
                form_name = "Lemon Cream"
            case '16':
                form_name = "Salted Cream"
            case '17':
                form_name = "Ruby Swirl"
            case '18':
                form_name = "Caramel Swirl"
            case '19':
                form_name = "Rainbow Swirl"
    # Zacian Case
    elif (pokemon_id == '938'):
        match form_num:
            case '11':
                form_name = "Hero of Many Battles"
            case '12':
                form_name = "Crowned Sword"
    # Zamazenta Case
    elif (pokemon_id == '939'):
        match form_num:
            case '11':
                form_name = "Hero of Many Battles"
            case '12':
                form_name = "Crowned Shield"
    # Morpeko Case
    elif (pokemon_id == '941'):
        match form_num:
            case '11':
                form_name = "Full Belly Mode"
            case '12':
                form_name = "Hangry Mode"
    # Indeedee Case
    elif (pokemon_id == '942'):
        match form_num:
            case '00':
                form_name = "Male"
            case '01':
                form_name = "Female"
    # Eiscue Case
    elif (pokemon_id == "975"):
        match form_num:
            case '11':
                form_name = "Ice"
            case '12':
                form_name = "Noice"
    # Calyrex Case
    elif (pokemon_id == '986'):
        match form_num:
            case '12':
                form_name = "Ice Rider"
            case '13':
                form_name = "Shadow Rider"
    # Zarude Case
    elif (pokemon_id == '988'):
        match form_num:
            case '12':
                form_name = "Dada"
    # Sneasler Case
    elif (pokemon_id == '1003'):
        regional_form = ""
    # Enamorus Case
    elif (pokemon_id == '1004'):
        match form_num:
            case '11':
                form_name = "Incarnate Forme"
            case '12':
                form_name = "Therian Forme"
    # Overquil Case
    elif (pokemon_id == '1005'):
        regional_form = ""
    # Basculegion Case
    elif (pokemon_id == '1006'):
        regional_form = ""
        match form_num:
            case '11':
                form_name = "Male"
            case '12':
                form_name = "Female"
    # Ursaluna Case
    elif (pokemon_id == '1007'):
        match form_num:
            case '11':
                form_name = "Bloodmoon"
    # Oinkologne Case
    elif (pokemon_id == '1020'):
        match form_num:
            case '00':
                form_name = "Male"
            case '01':
                form_name = "Female"
    # Palafin Case
    elif (pokemon_id == '1038'):
        match form_num:
            case '11':
                form_name = "Zero Form"
            case '12':
                form_name = "Hero Form"
    # Maushold Case
    elif (pokemon_id == '1050'):
        match form_num:
            case '11':
                form_name = "Family of Three"
            case '12':
                form_name = "Family of Four"
    # Tatsugiri Case
    elif (pokemon_id == '1056'):
        match form_num:
            case '11':
                form_name = "Curly Form"
            case '12':
                form_name = "Droopy Form"
            case '13':
                form_name = "Stretch Form"
    # Squawkabilly Case
    elif (pokemon_id == '1064'):
        match var_num:
            case '00':
                form_name = "Green Plumage"
            case '01':
                form_name = "Blue Plumage"
            case '02':
                form_name = "Yellow Plumage"
            case '03':
                form_name = "White Plumage"
    # Gimmighoul Case
    elif (pokemon_id == '1080'):
        match form_num:
            case '11':
                form_name = "Chest Form"
            case '12':
                form_name = "Roaming Form"
    # Koraidon Case
    elif (pokemon_id == '1102'):
        match form_num:
            case '12':
                form_name = "Bike Mode"
    # Miraidon Case
    elif (pokemon_id == '1103'):
        match form_num:
            case '12':
                form_name = "Bike Mode"
    # Ogrepon Case
    elif (pokemon_id == '1120'):
        match form_num:
            case '11':
                form_name = "Teal Mask"
            case '12':
                form_name = "Wellspring Mask"
            case '13':
                form_name = "Hearthflame Mask"
            case '14':
                form_name = "Cornerstone Mask"
    # Terapagos Case
    elif (pokemon_id == '1130'):
        match form_num:
            case '11':
                form_name = "Normal Form"
            case '12':
                form_name = "Terastal Form"
            case '13':
                form_name = "Stellar Form"

    # String Formatting to Look Good
    if form_name != "":
        form_name = "(%s)" %form_name
    if regional_form != "":
        regional_form = "%s " %regional_form
    real_pokemon_id = pids.get(pokemon_name)
    # Rename Files
    directory = 'Pokemon Icons'
    file_path = os.path.join(directory, file_name)
    if (real_pokemon_id == None):
        print()
    new_file = os.path.join(directory, "%s-%s%s%s.png" % (real_pokemon_id, regional_form, pokemon_name, form_name))
    os.rename(file_path, new_file)

    # Trim the Whitespace
    
    # Open The Image
    image = Image.open(new_file)
    # Convert Image to RGBA (so it has an alpha channel)
    image = image.convert("RGBA")

    # Get bounding box of non-white areas
    bbox = image.getbbox()
    if bbox:
        # Crop the image to bounding box
        trimmed_image = image.crop(bbox)
        # Save the cropped image
        trimmed_image.save(new_file)




