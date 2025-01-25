import os
from functions import get_sort_ordered_list, get_cards, get_new_image, create_card
from flask import Flask, render_template, request, send_from_directory

lapp = Flask(__name__)

# Get inverse sorted image list
sort_order = get_sort_ordered_list()
# Get the cards dictionary in sorted order
the_cards = get_cards(sort_order)


# Application routing
@lapp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', the_cards=the_cards, new_image=get_new_image())


# favicon.ico
@lapp.route('/favicon.ico')
def favicon():
    print(lapp.root_path)
    return send_from_directory(os.path.join(lapp.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Card view
@lapp.route('/card-view/', methods=['GET'])
def card_view(image="Van-sedona.jpg"):

    print("card_view GET")
    image = request.args.get('image')
    return render_template('card.html', the_cards=the_cards, image=image)


# --------------------------UPDATE------------------------------- #
# Card update
@lapp.route('/card-update/', methods=['GET', 'POST'])
def card_update(image="Don_Simpson.jpg"):
    print("card_update POST")
    image = request.args.get('image')
    email = request.form['email']
    pwd = request.form['password']
    print(email)
    print(pwd)

    return render_template('card_edit.html', the_cards=the_cards, image=image)
# --------------------------UPDATE------------------------------- #


# Card edit
@lapp.route('/card-edit/', methods=['GET', 'POST'])
def card_edit(image="Van-sedona.jpg"):
    print("card_edit GET")
    image = request.args.get('image')

    return render_template('card_edit.html', the_cards=the_cards, image=image)


# Get thumbnail image
@lapp.route('/thumb/', methods=['GET'])
def thumb(image="Van-sedona.jpg"):
    image_request = request.args.get('image')

    if image_request:
        image = image_request

    return render_template('thumb.html', image=image)


# Add image
@lapp.route('/add-image/', methods=['GET', 'POST'])
def add_image(image="Van-sedona.jpg"):
    image_request = request.args.get('image')
    print("IN add_image")
    print(image_request)
    print("IN add_image")
    dictionary = create_card(image_request)
    print(dictionary)

    if image_request:
        image = image_request

    return render_template('add-image.html', image=image)


if __name__ == '__main__':
    lapp.run(host="0.0.0.0", debug=True)
