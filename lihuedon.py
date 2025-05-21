import os
import io
import requests
from flask import Flask, render_template, request, Response, send_from_directory, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

# Application packages
from functions import get_sort_ordered_list, get_cards, get_date_time, allowed_file, get_new_image, create_new_card, update_card, delete_card, get_dash_cards, get_json_key_value, get_svg_image_names
from users import load_users, save_users
from loan import Loan
from geonames import get_zip_data
from weather import BarometerBaseline

session = requests.Session()
session.cookies['zip'] = "98225"
session.cookies['baseline'] = 28.45
# print(session.cookies.get_dict())

fig = Figure()
ln = Loan()

lapp = Flask(__name__)
# lapp.config['SECRET_KEY'] = get_json_key_value('key')
lapp.secret_key = get_json_key_value('key')
lapp.inHg_conversion_factor = 33.8639
lapp.base_url =  get_json_key_value('base_url')
lapp.baseline = None

login_manager = LoginManager()
login_manager.init_app(lapp)

# Load users from the file when the application starts
lapp_users = load_users()

# User model
class User(UserMixin):
    def __init__(self, id, password_hash):
        self.id = id
        self.password_hash = password_hash

# User loader
@login_manager.user_loader
def load_user(user_id):
    if user_id in lapp_users:
        user_data = lapp_users[user_id]
        return User(user_id, user_data["password_hash"])
    return None

# Get inverse sorted image list
sort_order = get_sort_ordered_list()


# Get the cards dictionary in sorted order
the_cards = get_cards(sort_order)

# Get dashboard card sorted names list
dash_sort_order = ['d-weather', 'd-clock', 'd-svg', 'd-clock-london', 'd-widget']
# Get the cards dictionary in sorted order
dash_cards = get_dash_cards(dash_sort_order)

# Define the path to save uploaded files
UPLOAD_FOLDER = 'static/images/'
lapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def set_baseline(pressure_inHg, reset):

    if not lapp.baseline:
        lapp.baseline = BarometerBaseline(pressure_inHg, get_date_time(True))
        session.cookies['baseline'] = pressure_inHg

    elif reset:
        lapp.baseline.set_pressure(pressure_inHg)
        lapp.baseline.set_timestamp(get_date_time(True))
        session.cookies['baseline'] = pressure_inHg


# Application routing
@lapp.route('/', methods=['GET', 'POST'])
def index():
    lapp.logger.info('Home page was accessed.')  # Log an INFO message
    return render_template('index.html', the_cards=the_cards, dash_cards=dash_cards)


# favicon.ico
@lapp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(lapp.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@lapp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in lapp_users:
            return "Username already exists!"
        password_hash = generate_password_hash(password)  # Hash the password
        lapp_users[username] = {"password_hash": password_hash}  # Store user in JSON-compatible format
        save_users(lapp_users)  # Save the updated users to the file
        return redirect(url_for('login'))
    return render_template('register.html')


@lapp.route('/login', methods=['GET', 'POST'])
def login():
    new_image = get_new_image()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_data = lapp_users.get(username)
        if user_data and check_password_hash(user_data["password_hash"], password):  # Verify the password
            user = User(username, user_data["password_hash"])
            login_user(user)
            return render_template('card_edit.html', image='Don_Simpson.jpg', the_cards=the_cards, image_list=sort_order, new_image=new_image, dash_cards=dash_cards)
        # return render_template('login.html')
        return "Invalid username or password!"
    return render_template('login.html')


@lapp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@lapp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template("dashboard.html", dash_cards=dash_cards)


# Dash view
@lapp.route('/dash-view/', methods=['GET'])
def dash_view(image=None):
    name = request.args.get('name')
    template_name = name + ".html"
    image = dash_cards[name].get("image")
    svg_images = get_svg_image_names() # used for svg demo widget
    return render_template(template_name, dash_cards=dash_cards, image=image, name=name, svg_images=svg_images)


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
    # print(city_info)
    if city_info:
        city = city_info['postalCodes'][0]['placeName']
        state = city_info['postalCodes'][0]['adminName1']
    # print(city)
    final_url = lapp.base_url + zip + ",us"
    json_data = requests.get(final_url).json()
    the_weather = json_data['weather']
    the_main = json_data['main']
    # print(the_main)
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


# Card view
@lapp.route('/card-view/', methods=['GET'])
def card_view(image=None):
    image = request.args.get('image')
    return render_template('card.html', the_cards=the_cards, image=image, dash_cards=dash_cards)


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
    return render_template('loan-gui.html', PV=PV, rate=rate, number=number, payment=payment, display=display, dash_cards=dash_cards)


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
@login_required
def card_edit(image=None):
    sort_order = get_sort_ordered_list()
    image = request.args.get('image')
    new_image = get_new_image()
    return render_template('card_edit.html', the_cards=the_cards, image=image, image_list=sort_order, new_image=new_image, dash_cards=dash_cards)


# Get thumbnail image
@lapp.route('/thumb/', methods=['GET'])
def thumb(image=None):
    image_request = request.args.get('image')
    if image_request:
        image = image_request
    return render_template('thumb.html', image=image)


# Get thumbnail svg image
@lapp.route('/thumb-svg/', methods=['GET'])
def thumb_svg(image=None):
    image_request = request.args.get('image')
    if image_request:
        image = image_request
    return render_template('thumb_svg.html', image=image)


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
    global sort_order
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
