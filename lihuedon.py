import os
import io
import time
import requests
from datetime import datetime

from functions import get_sort_ordered_list, get_cards, get_new_image, create_new_card, update_card, delete_card, get_dash_cards, get_json_key_value
from flask import Flask, render_template, request, Response, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from loan import Loan
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import logging
from geonames import get_zip_data
# from uszipcode import SearchEngine
# import uszipcode as uszip
# import sqlalchemy_mate
# http://api.geonames.org/findNearbyPostalCodesJSON?country=US&radius=1&username=lihuedon&postalcode=98225

# sr = uszip.SearchEngine()

# z = sr.by_zipcode("10001")
# print(z)
#
# z = sr.by_zipcode(10001)
# print(z)

session = requests.Session()

print(session.cookies.get_dict())

session.cookies['zip'] = "98225"
session.cookies['baseline'] = 28.45

fig = Figure()

ln = Loan()

lapp = Flask(__name__)
# lapp.config['SECRET_KEY'] = get_json_key_value('key')
lapp.inHg_conversion_factor = 33.8639
lapp.base_url =  get_json_key_value('base_url')
lapp.baseline = None

# Configure logging
logging.basicConfig(
    filename='/home/pi/gunicorn/gunicorn_access.log',  # Log file name
    level=logging.INFO,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

# Get inverse sorted image list
sort_order = get_sort_ordered_list()
# Get the cards dictionary in sorted order
the_cards = get_cards(sort_order)

# Get dashboard card sorted names list
dash_sort_order = ['d-weather', 'd-clock', 'd-clock-london']
# Get the cards dictionary in sorted order
dash_cards = get_dash_cards(dash_sort_order)

# Define the path to save uploaded files
UPLOAD_FOLDER = 'static/images/'
lapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def get_date_time(time=None):
    x = datetime.now()
    dt_string = x.strftime("%A") + " " + x.strftime("%B") + " " + x.strftime("%d") + ", " + x.strftime("%Y")
    if time:
        dt_string = dt_string + " " + x.strftime("%X")
    return dt_string


class BarometerBaseline:
    def __init__(self, pressure, timestamp):
        self._pressure = pressure
        self._timestamp = timestamp

    def get_pressure(self):
        return self._pressure

    def set_pressure(self, value):
        self._pressure = value

    def get_timestamp(self):
        return self._timestamp

    def set_timestamp(self, value):
        self._timestamp = value


def set_baseline(pressure_inHg, reset):

    if not lapp.baseline:
        lapp.baseline = BarometerBaseline(pressure_inHg, get_date_time(True))
        session.cookies['baseline'] = pressure_inHg

    elif reset:
        lapp.baseline.set_pressure(pressure_inHg)
        lapp.baseline.set_timestamp(get_date_time(True))
        session.cookies['baseline'] = pressure_inHg


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def stream_log():
    log_file_path = "/home/pi/gunicorn/gunicorn_access.log"
    with open(log_file_path) as log_file:
        # Move to the end of the file
        log_file.seek(0, 2)
        while True:
            line = log_file.readline()
            if line:
                yield f"{line}"
            time.sleep(.5)  # Small delay for stream pacing


# def validate_zip(zip_code):
#     search = SearchEngine()
#     return search.by_zipcode(zip_code)


# Application routing
@lapp.route('/', methods=['GET', 'POST'])
def index():
    lapp.logger.info('Home page was accessed.')  # Log an INFO message
    return render_template('index.html', the_cards=the_cards)


@lapp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template("dashboard.html", dash_cards=dash_cards)


# Dash view
@lapp.route('/dash-view/', methods=['GET'])
def dash_view(image=None):
    name = request.args.get('name')
    template_name = name + ".html"
    image = dash_cards[name].get("image")
    return render_template(template_name, dash_cards=dash_cards, image=image, name=name)


# favicon.ico
@lapp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(lapp.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@lapp.route('/weather/', methods=['GET'])
def weather(zip="98225"):
    tempbaseline = session.cookies['baseline']
    zip_request = request.args.get('zip')
    zip_cookie = session.cookies['zip']
    if zip_request:
        zip = zip_request
        session.cookies['zip'] = zip_request
    elif zip_cookie:
        zip = zip_cookie
    city = "Bellingham"  #default
    state = "Washington"  #default
    city_info = get_zip_data(zip)
    print(city_info)
    if city_info:
        city = city_info['postalCodes'][0]['placeName']
        state = city_info['postalCodes'][0]['adminName1']
    print(city)
    final_url = lapp.base_url + zip + ",us"
    json_data = requests.get(final_url).json()
    the_weather = json_data['weather']
    the_main = json_data['main']
    print(the_main)
    zip_request = the_main['temp']
    feels_like = the_main['feels_like']
    temp_min = the_main['temp_min']
    temp_max = the_main['temp_max']
    pressure = the_main['pressure']
    humidity = the_main['humidity']
    pressure_inHg = round(pressure/lapp.inHg_conversion_factor, 2)
    reset = request.args.get('reset')
    set_baseline(pressure_inHg, reset)
    return render_template('weather.html', baseline=lapp.baseline, city=city, state=state, zip=zip, temp=zip_request, the_weather=the_weather, feels_like=feels_like, temp_min=temp_min, temp_max=temp_max, pressure=pressure, pressure_inHg=pressure_inHg, humidity=humidity)


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


@lapp.route('/error')
def error():
    lapp.logger.error('Error occurred in /error route.')  # Log an ERROR message
    return "This route throws an error!", 500


@lapp.route('/stream')
def stream():
    return Response(stream_log(), content_type='text/event-stream')


# Card view
@lapp.route('/card-view/', methods=['GET'])
def card_view(image=None):
    image = request.args.get('image')
    return render_template('card.html', the_cards=the_cards, image=image)


# Loan Calculator
@lapp.route('/loan-calculator/', methods=['GET'])
def loan_gui():
    PV = request.args.get('PV')
    rate = request.args.get('rate')
    number = request.args.get('number')
    payment = "ANSWER GOES HERE"
    display = ""
    if PV:
        payment = ln.calculate_payment(int(PV), float(rate), int(number))
        display = ln.present_payment(payment, int(PV), float(rate), int(number))
    return render_template('loan-gui.html', PV=PV, rate=rate, number=number, payment=payment, display=display)


# Get Loan Header
@lapp.route('/loan-header/', methods=['GET'])
def get_loan_header():
    return ln.print_header()


# Plot Loan
@lapp.route('/plot_loan', methods=['GET'])
def plot_loan():
    """Take loan data and graph amortization, payment, interest, and principle."""
    #  def plot_loan(self, P, PV, r, n):
    P = float(request.args.get('P'))
    PV = float(request.args.get('PV'))
    r = float(request.args.get('r'))
    n = int(request.args.get('n'))
    principle = PV
    rate = r * .01
    num_payments = n
    monthly_payment = P
    x_payment_numbers = []
    y_monthly_payments = []
    y_interest_values = []
    y_principle_values = []
    for payment_no in range(1, num_payments + 1):
        x_payment_numbers.append(payment_no)
        y_monthly_payments.append(monthly_payment)
        int_pmt = principle * rate / 12
        y_interest_values.append(int_pmt)
        princ_pmt = monthly_payment - int_pmt
        y_principle_values.append(princ_pmt)
        principle -= princ_pmt
    fig = Figure(figsize=(11, 8.5))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)  # Add a subplot at position 1x1x1 (grid of 1 row, 1 col)
    ax.plot(x_payment_numbers, y_principle_values, linewidth=3, color='yellow')
    ax.plot(x_payment_numbers, y_interest_values, linewidth=3, color='cyan')
    ax.plot(x_payment_numbers, y_monthly_payments, linewidth=1, color='magenta')
    # Set chart title and label axes
    ax.set_title(f"{ln.prepare_plot_title(P, PV, r, n)}", fontsize=14)
    ax.set_xlabel("Number of Payments", fontsize=14)
    ax.set_ylabel("Principle and Interest", fontsize=14)
    # Set size of tick labels.
    ax.tick_params(axis='both', labelsize=14)
    # Save it to a BytesIO buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')


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


# Card edit
@lapp.route('/card-edit/', methods=['GET', 'POST'])
def card_edit(image=None):
    sort_order = get_sort_ordered_list()
    image = request.args.get('image')
    new_image = get_new_image()
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
