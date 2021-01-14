from flask import Flask
from flask import render_template, request, flash, redirect
from config import Config
from forms import LoginForm  # Temporary for testing form with Bootstrap
from booking import BookingForm, Booking
from mongodb import MongoDb
from datetime import datetime
from sendsms import SendSms
# import logging


flaskapp = Flask(__name__)
config = Config()
flaskapp.config.from_object(config)
mongo = MongoDb(flaskapp.config['MONGO_DB'], flaskapp.config['DATABASE'], flaskapp.config['COLLECTION'])

# if __name__ != '__main__':
#     gunicorn_logger = logging.getLogger('gunicorn.error')
#     flaskapp.logger.handlers = gunicorn_logger.handlers
#     flaskapp.logger.setLevel(gunicorn_logger.level)

def getBookedDays():
    bookedDays = []
    for booking in mongo.get({'roomName': 'Elodie'}):
        bookedDays += [[booking['startDate'].strftime('%Y-%m-%d'),booking['endDate'].strftime('%Y-%m-%d')]]
    return bookedDays

def getBookingForm():
    form = BookingForm()
    if form.validate_on_submit():
        # print('Form validated')
        # flaskapp.logger.debug('this is a DEBUG message')
        # flaskapp.logger.info('this is an INFO message')
        # flaskapp.logger.warning('this is a WARNING message')
        # flaskapp.logger.error('this is an ERROR message')
        # flaskapp.logger.critical('this is a CRITICAL message')
        # flash('Got booking for user name={}, mail={}, startDate={}, endDate={}'.format(
        #     form.name.data, form.mail.data, form.startDate.data, form.endDate.data))
        # Register this booking in database
        mongo.add({
            'roomName': 'Elodie',
            'startDate': datetime.strptime(form.startDate.data, '%Y-%m-%d'), # datetime(form.startDate.data),
            'endDate': datetime.strptime(form.endDate.data, '%Y-%m-%d'), #form.endDate.data,
            'customerName': form.name.data,
            'customerMail': form.mail.data,
            'customerPhone': form.phone.data
        })
        if flaskapp.config['OS_NAME'] != 'nt':  # Send SMS message only on Linux
            # Send confirmation SMS to us
            msg = 'Réservation du ' + form.startDate.data[0:12] + ' au ' + form.endDate.data[0:12] + '\r\n' + \
            'Nom: ' + form.name.data + '\r\n' \
            'Phone: ' + form.phone.data + '\r\n' \
            'Mail: ' + form.mail.data + '\r\n'
            sendSms = SendSms()
            sendSms.sendMessage(msg)
    else:
        for error in form.startDate.errors:
            print('startdate Error', error)
        for error in form.endDate.errors:
            print('enddate Error', error)
        for error in form.name.errors:
            print('name Error', error)
        for error in form.mail.errors:
            print('mail Error', error)
        for error in form.phone.errors:
            print('phone Error', error)


    return form

@flaskapp.route('/', methods=['GET', 'POST'])
def index():
    bookedDays = getBookedDays()
    form = getBookingForm()
    if form.validate_on_submit():
        booking = Booking(form.startDate.data[0:12], form.endDate.data[0:12], "Room to manage later", form.name.data, form.mail.data, form.phone.data)
        return render_template('confirmation.html', booking=booking)
    return render_template('index.html', form=form, bookedDays=bookedDays)

@flaskapp.route('/mobile', methods=['GET', 'POST'])
def mobile():
    bookedDays = getBookedDays()
    form = getBookingForm()
    return render_template('mobile.html', form=form, bookedDays=bookedDays)

@flaskapp.route('/confirmation')
def confirmation():
    bookedDays = getBookedDays()
    form = getBookingForm()
    return render_template('confirmation.html', form=form, bookedDays=bookedDays)

@flaskapp.route('/bookinglist')
def bookinglist():
    bookingList = []
    for bookingRecord in mongo.get({'roomName': 'Elodie'}):
        booking = Booking(bookingRecord['startDate'], bookingRecord['endDate'], bookingRecord['roomName'], bookingRecord['customerName'], bookingRecord['customerMail'], bookingRecord['customerPhone'])
        bookingList += [booking]
    return render_template('bookinglist.html', bookingList=bookingList)

@flaskapp.route('/test', methods=['GET', 'POST'])
def test():
    form = BookingForm()
    if form.validate_on_submit():
        flash('Got booking for user name={}, mail={}'.format(
            form.name.data, form.mail))
    return render_template('test.html', form=form)    

@flaskapp.route('/test2', methods=['GET', 'POST'])
def test2():
    form = BookingForm()
    if form.validate_on_submit():
        flash('Got booking for user name={}, mail={}'.format(
            form.name.data, form.mail))
    return render_template('test2.html', form=form)    


@flaskapp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/')
    return render_template('login.html', title='Sign In', form=form)