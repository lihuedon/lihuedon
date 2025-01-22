import os
from functions import get_image_names, get_sort_ordered_list, get_cards, get_new_image, create_card
from flask import Flask, render_template, request, send_from_directory

lapp = Flask(__name__)

# The image list drives the home content
image_names = get_image_names()
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
@lapp.route('/card-view/', methods=['GET', 'POST'])
def card_view(image="Van-sedona.jpg"):
    image_request = request.args.get('image')

    if image_request:
        image = image_request

    return render_template('card.html', the_cards=the_cards, image=image)


# Card edit
@lapp.route('/card-edit/', methods=['GET', 'POST'])
def card_edit(image="Van-sedona.jpg"):
    image_request = request.args.get('image')

    return render_template('card_edit.html', the_cards=the_cards, image=image_request)


# Get thumbnail image
@lapp.route('/thumb/', methods=['GET', 'POST'])
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


# BOOTSTRAP ALBUM EXAMPLE CODE
@lapp.route('/album/', methods=['GET', 'POST'])
def album():
    return render_template('bootstrap/album/index.html')


if __name__ == '__main__':
    lapp.run(host="0.0.0.0", debug=True)
