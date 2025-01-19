import os
from functions import get_cards
from flask import Flask, render_template, request, send_from_directory

lapp = Flask(__name__)

# The image list drives the home content
#   image_names = get_image_names()
# Get inverse sorted image list
#   sort_order = get_sort_order(image_names)
# Get the cards dictionary in sorted order
the_cards = get_cards()


# Application routing
@lapp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', the_cards=the_cards)


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

    if image_request:
        image = image_request

    return render_template('card_edit.html', the_cards=the_cards, image=image)


# Get thumbnail image
@lapp.route('/thumb/', methods=['GET', 'POST'])
def thumb(image="Van-sedona.jpg"):
    image_request = request.args.get('image')

    if image_request:
        image = image_request

    return render_template('thumb.html', image=image)


# BOOTSTRAP ALBUM EXAMPLE CODE
@lapp.route('/album/', methods=['GET', 'POST'])
def album():
    return render_template('bootstrap/album/index.html')


if __name__ == '__main__':
    lapp.run(host="0.0.0.0", debug=True)
