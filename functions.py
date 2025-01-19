import os
import json


def get_image_names():
    # The images drive the home content
    image_path = '/home/pi/PycharmProjects/lihuedon/static/images'
    image_names = os.listdir(image_path)
    print(image_names)
    return image_names


# Determine image sort order by id reversed
def get_sort_order():
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
            print("IMAGE NOT FOUND: " + file_path+image_name)
    i += 1

    not_ordered.sort(reverse=True)

    for item in not_ordered:
        a, b = item.split("=")
        sorted.append(b)

    print(sorted)

    return sorted


# There is one card per image
def get_cards():
    sort_order = get_sort_order()
    # Read json file
    cards ={}
    i = 1
    for image_name in sort_order:
        with open("app_json/" + image_name + ".json", mode="r", encoding="utf-8") as read_file:
            card_data = json.load(read_file)
            cards[image_name] = card_data
    i += 1

    return cards


def update_card(image="kitchen2.jpg"):

    file_path = "app_json/" + image + ".json"

    if os.path.exists(file_path):
        print('File exists: ' + file_path)

        with open(file_path, 'r+', encoding='utf-8') as json_file:
            card = json.load(json_file)

            card['id'] = 1
            card['name'] = "ClarkMansionInterior.jpg"
            card['title'] = "Grand Victorian Entry"
            card['create_dt'] = "1/18/2025"
            card['city'] = "London"
            # print(card['paragraphs'][0]['paragraph'])
            # print(card['paragraphs'][1]['paragraph'])

            i = 0
            new_text = ["Groovy Victorian Foyer", "Second paragraph", "Third paragraph modified also", "Something/Anything", "FIVE!"]
            # new_text = ["Wow! What a sunset!", "Second paragraph", "Third paragraph modified also", "ghjkkkk", "hbjhoibkj"]
            print(len(new_text))
            paras = card['paragraphs']
            print(len(paras))
            if i < len(paras):
                print("TO DO: FIX UPDATE_CARD FUNCTION")

            for txt in new_text:
                if i < len(paras):
                    card['paragraphs'][i]['paragraph'] = txt
                else:
                    print("TO DO: FIGURE OUT HOW TO ADD ANOTHER PARAGRAPH")
                    print(txt)
                    # card['paragraphs'][i]['paragraph'] = txt
                    # this statement blows chunks!
                    # IndexError: list index out of range

                i += 1

            # place the cursor at the beginning of the file
            json_file.seek(0)

            json.dump(card, json_file)
            json_file.truncate()

    else:
        print('File ' + file_path + ' does not exist.')
        return 1

    return card

print(update_card("ClarkMansionInterior.jpg"))