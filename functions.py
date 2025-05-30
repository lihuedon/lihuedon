import os
import json
from datetime import datetime

the_cards = {}
CREATE_CARD = "none"


# Define allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Get image names from file system
def get_image_names():
    # The images drive the home content
    image_path = './static/images'
    image_names = os.listdir(image_path)
    return image_names


def get_date_time(time=None):
    x = datetime.now()
    dt_string = x.strftime("%A") + " " + x.strftime("%B") + " " + x.strftime("%d") + ", " + x.strftime("%Y")
    if time:
        dt_string = dt_string + " " + x.strftime("%X")
    return dt_string


# Get next id number
def get_next_id_int():
    image_dictionary_reverse = get_sort_ordered_dict()
    my_keys = image_dictionary_reverse.keys()
    i = list(my_keys)[0]
    return i + 1


# Determine image sort order by id reversed
def get_sort_ordered_list():
    image_names = get_image_names()
    file_path = "app_json/"
    cards = {}
    not_ordered = []
    sorted = []
    i = 1
    for image_name in image_names:
        if os.path.exists(file_path + image_name + ".json"):
            with open("app_json/" + image_name + ".json", mode="r", encoding="utf-8") as read_file:
                card_data = json.load(read_file)
                cards[image_name] = card_data
                id = cards[image_name].get("id")
                image = cards[image_name].get("name")
                key = str(id) + "=" + image
                not_ordered.append(key)
        else:
            print("IMAGE JSON NOT FOUND: " + file_path+image_name)
            global CREATE_CARD
            CREATE_CARD = image_name
        i += 1
    return sort_list(not_ordered)


# Determine image sort order by id reversed
def get_sort_ordered_dict():
    image_names = get_image_names()
    file_path = "app_json/"
    cards = {}
    not_ordered = []
    sorted = []
    i = 1
    for image_name in image_names:
        if os.path.exists(file_path + image_name + ".json"):
            with open("app_json/" + image_name + ".json", mode="r", encoding="utf-8") as read_file:
                card_data = json.load(read_file)
                cards[image_name] = card_data
                id = cards[image_name].get("id")
                image = cards[image_name].get("name")
                key = str(id) + "=" + image
                not_ordered.append(key)
        else:
            print("IMAGE JSON NOT FOUND: " + file_path+image_name)
            global CREATE_CARD
            CREATE_CARD = image_name
        i += 1
    return sort_dict(not_ordered)


def sort_list(unsorted_list=[]):
    # unsorted_list = ['2=kitchen2.jpg', '4=trump.jpg', '6=violin.gif', '2=sunset.jpg', '1=ClarkMansionInterior.jpg', '5=Van-sedona.jpg']
    unsorted_dict = {}
    sorted_list =[]
    for item in unsorted_list:
        a, b = item.split("=")
        i = int(a)
        unsorted_dict[i] = b
    my_keys = list(unsorted_dict.keys())
    my_keys.sort(reverse=True)
    # Sorted Dictionary
    sd = {i: unsorted_dict[i] for i in my_keys}
    for i in my_keys:
        sorted_list.append(sd[i])
    return sorted_list


def sort_dict(unsorted_list=[]):
    # unsorted_list = ['2=kitchen2.jpg', '4=trump.jpg', '6=violin.gif', '2=sunset.jpg', '1=ClarkMansionInterior.jpg', '5=Van-sedona.jpg']
    unsorted_dict = {}
    sorted_list =[]
    for item in unsorted_list:
        a, b = item.split("=")
        i = int(a)
        unsorted_dict[i] = b
    my_keys = list(unsorted_dict.keys())
    my_keys.sort(reverse=True)
    # Sorted Dictionary
    sorted_dictionary = {i: unsorted_dict[i] for i in my_keys}
    for i in my_keys:
        sorted_list.append(sorted_dictionary[i])
    return sorted_dictionary


# There is one card per image
def get_cards(sort_order=[]):
    # Read json file
    cards ={}
    i = 1
    for image in sort_order:
        file_path = "app_json/" + image + ".json"
        if os.path.exists(file_path):
            with open(file_path, mode="r", encoding="utf-8") as read_file:
                card_data = json.load(read_file)
                cards[image] = card_data
        else:
            print("NOT FOUND")
            print(file_path)
    i += 1
    return cards


# There is one card per image
def get_dash_cards(sort_order=[]):
    # Read json file
    cards ={}
    i = 1
    for name in sort_order:
        file_path = "dash_json/" + name + ".json"
        if os.path.exists(file_path):
            with open(file_path, mode="r", encoding="utf-8") as read_file:
                card_data = json.load(read_file)
                cards[name] = card_data
        else:
            print("NOT FOUND")
            print(file_path)
    i += 1
    return cards


def update_card(image=None, id=None, name=None, title=None, paragraph_text=None, city=None):
    card = {}
    paragraphs = []
    paragraph = {}
    file_path = ""
    if image != None:
        file_path = "app_json/" + image + ".json"
    if os.path.exists(file_path):
        with open(file_path, 'r+', encoding='utf-8') as json_file:
            card = json.load(json_file)
            if id != None:
                card['id'] = id
            if name !=None:
                card['name'] = name
            if title != None:
                card['title'] = title
            if city != None:
                card['city'] = city
            if paragraph_text != None:
                # CREATE DICTIONARY
                dict_list = []
                i = 0
                for p in paragraph_text:
                    paragraph['paragraph'] = p
                    dict_copy = paragraph.copy()
                    dict_list.append(dict_copy)
                i += 1
                card['paragraphs'] = dict_list
            # place the cursor at the beginning of the file
            json_file.seek(0)
            json.dump(card, json_file)
            json_file.truncate()
    else:
        print('File ' + file_path + ' does not exist.')
        return 1
    return card


# Create new json card file
def create_new_card(image=None):
    card = {}
    paragraphs = []
    paragraph = {}
    json_file_path = "app_json/" + image + ".json"
    # Get the current date and time
    now = datetime.now()
    # Format the date and time
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    print("Formatted date and time:", formatted_now)
    card['id'] = get_next_id_int()
    card['name'] = image
    card['title'] = "Title Goes Here"
    card['create_dt'] = formatted_now
    card['city'] = "Bellingham"
    paragraph_text = ["First paragraph", "Second paragraph", "", "", "", "", "", "", "", ""]
    # CREATE DICTIONARY
    dict_list = []
    i = 0
    for p in paragraph_text:
        paragraph['paragraph'] = p
        dict_copy = paragraph.copy()
        dict_list.append(dict_copy)
    i += 1
    card['paragraphs'] = dict_list
    print(card)
    with open(json_file_path, 'w') as fp:
        json.dump(card, fp)
    global CREATE_CARD
    CREATE_CARD = "none"
    return card


def get_new_image():
    global CREATE_CARD
    return CREATE_CARD


# The delete card's JSON file
def delete_card_json(image=None, name=None):
    print(image)
    print(name)
    # Read json file
    file_path = "app_json/" + image + ".json"
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print("File was removed.")
        else:
            print("File does not exist but it's definitely gone.")
    except Exception as e:
        print(e)
    finally:
        print("delete_card_json: " + file_path)
    return 0


# The delete card's image file
def delete_card_image(image=None):
    print(image)
    # Read image file
    file_path = "./static/images/" + image
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print("File was removed.")
        else:
            print("File does not exist but it's definitely gone.")
    except Exception as e:
        print(e)
    finally:
        print("delete_card_image: " + file_path)
    return 0


# delete card image and json file
def delete_card(image=None):
    delete_card_json(image=image)
    delete_card_image(image=image)
    return "CARD DELETED: " + image


# Load JSON data from a file
def get_json_key_value(key=""):
    with open('./static/lapp.json') as file:
        json_data = json.load(file)
    value = json_data[key]
    return value

# Get svg images for svg widget
def get_svg_image_names():
    # Specify the directory
    directory = 'static/svg'
    # List all files
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    # Print the list of files
    # print("Files in the directory:")
    # for file in files:
    #     print(file)
    return files


# print(f"The value for '{key}' is: {value}")

# message = delete_card()
# print(message)

# # The image list drives the home content
# # Get inverse sorted image list
# sort_order = get_sort_ordered_list()
# print(sort_order)
# # Get the cards dictionary in sorted order
# the_cards = get_cards(sort_order)

# new_card = create_new_card(image="Don_Simpson.jpg")
# print(new_card)
#
# print(get_next_id_int())
