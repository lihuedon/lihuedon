import os

from repolib.util import keys_map

from functions import get_sort_ordered_list, get_cards, get_new_image, create_new_card, update_card, delete_card
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from loan import Loan

ln = Loan()


lapp = Flask(__name__)

# Get inverse sorted image list
sort_order = get_sort_ordered_list()
# Get the cards dictionary in sorted order
the_cards = get_cards(sort_order)


# Define the path to save uploaded files
UPLOAD_FOLDER = 'static/images/'
lapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_payment():
    """Validate input, calculate payment, and return formatted results."""
    # print(ln.print_header())
    # while True:
        # if not input_present_value.value.replace(".", "").isdigit():
        #     error("Input error", "You must type a valid loan amount.")
        #     break
        # elif not input_rate.value.replace(".", "").isdigit():
        #     error("Input error", "You must type a valid interest rate.")
        #     break
        # elif not input_period.value.isdigit():
        #     error("Input error", "You must type a valid number of months.")
        #     break
        # else:
        #     PV = float(input_present_value.value)
        #     r = float(input_rate.value)
        #     n = int(input_period.value)
        #     P = ln.calculate_payment(PV, r, n)
        #     display.value = "%s" % ln.prepare_plot_title(P, PV, r, n)
        #     plot_button.update_command(_plot, args=[P, PV, r, n])
        #     plot_button.show()
        #     plot_button.focus()
        #     break
    return ln.print_header()

# print(calculate_payment())

@lapp.route('/upload_form', methods=['GET'])
def upload_form():
    return render_template('upload.html')


@lapp.route('/upload', methods=['POST'])
def upload_file():
    new_name = request.form['new-name']
    print(new_name)
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Rename the file from the input
        new_filename = new_name
        file.save(os.path.join(lapp.config['UPLOAD_FOLDER'], new_filename))
        return redirect(url_for('uploaded_file', filename=new_filename))


@lapp.route('/uploads/<filename>')
def uploaded_file(filename):
    return f'File successfully uploaded: {filename}'


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
@lapp.route('/card-view/', methods=['GET'])
def card_view(image=None):

    print("card_view GET")
    image = request.args.get('image')
    return render_template('card.html', the_cards=the_cards, image=image)


# Loan Calculator
@lapp.route('/loan-calculator/', methods=['GET'])
def loan_gui():
    print("loan_gui GET")
    PV = request.args.get('PV')
    print(PV)
    rate = request.args.get('rate')
    print(rate)
    number = request.args.get('number')
    print(number)
    payment = "ANSWER GOES HERE"
    display = "FORMATTED DISPLAY"
    if PV:
        payment = ln.calculate_payment(int(PV), float(rate), int(number))
        display = ln.present_payment(payment, int(PV), float(rate), int(number))
    print(payment)

    return render_template('loan-gui.html', PV=PV, rate=rate, number=number, payment=payment, display=display)


# Get Loan Header
@lapp.route('/loan-header/', methods=['GET'])
def get_loan_header():

    return ln.print_header()

# --------------------------UPDATE------------------------------- #
# Card update
@lapp.route('/card-update/', methods=['GET', 'POST'])
def card_update(image=None):
    print("card_update POST")

    image = request.args.get('image')
    id = request.form['id']  # name='id'
    name = request.form['name']  # name='name'
    title = request.form['title']  # name='title'
    paragraphs = request.form.getlist('paragraphs[]')  # name='paragraphs[]'
    if image != name:
        print(image)
        print(name)
        # TO DO
        # delete_card_json(image)
        # card = create_card(image=name, id=id, title=title)
    else:
        card = update_card(image=image, id=id, name=name, title=title, paragraph_text=paragraphs)
    print(card)

    global the_cards
    sort_order = get_sort_ordered_list()
    the_cards = get_cards(sort_order)

    return render_template('card_edit.html', the_cards=the_cards, image=image, image_list=sort_order, new_image=get_new_image())
# --------------------------UPDATE------------------------------- #


# Card edit
@lapp.route('/card-edit/', methods=['GET', 'POST'])
def card_edit(image=None):
    print("card_edit GET")
    sort_order = get_sort_ordered_list()
    image = request.args.get('image')
    new_image = get_new_image()
    print(new_image)

    return render_template('card_edit.html', the_cards=the_cards, image=image, image_list=sort_order, new_image=new_image)


# Get thumbnail image
@lapp.route('/thumb/', methods=['GET'])
def thumb(image=None):
    image_request = request.args.get('image')

    if image_request:
        image = image_request

    return render_template('thumb.html', image=image)


# Add image
@lapp.route('/add-image/', methods=['GET', 'POST'])
def add_image(image=None):
    image_request = request.args.get('image')
    print("IN add_image")
    print(image_request)
    dictionary = create_new_card(image_request)

    if image_request:
        image = image_request
    new_image = get_new_image()

    global the_cards
    sort_order = get_sort_ordered_list()
    the_cards = get_cards(sort_order)

    return render_template('card_edit.html', image=image, the_cards=the_cards, image_list=sort_order, new_image=new_image)


# delete card
@lapp.route('/delete-card/', methods=['GET', 'POST'])
def delete_this_card(image=None):
    image_request = request.args.get('image')
    print("IN delete_card")
    print(image_request)
    new_image = get_new_image()
    message = delete_card(image_request)
    print(message)

    global the_cards
    sort_order = get_sort_ordered_list()
    the_cards = get_cards(sort_order)

    return render_template('card_edit.html', image='Don_Simpson.jpg', the_cards=the_cards, image_list=sort_order, new_image=new_image)


if __name__ == '__main__':
    lapp.run(host="0.0.0.0", debug=True)
