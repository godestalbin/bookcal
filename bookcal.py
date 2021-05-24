from flask import Flask
from flask import render_template, request, flash, redirect
from config import Config
from forms import LoginForm  # Temporary for testing form with Bootstrap
from booking import BookingForm, Booking
from mongodb import MongoDb
from datetime import datetime
from sendsms import SendSms
from sendmail import SendMail
# import logging


flaskapp = Flask(__name__)
config = Config()
flaskapp.config.from_object(config)
mongo = MongoDb(flaskapp.config['MONGO_DB'], flaskapp.config['DATABASE'], flaskapp.config['COLLECTION'])
mongoRooms = MongoDb(flaskapp.config['MONGO_DB'], flaskapp.config['DATABASE'], 'rooms')

# if __name__ != '__main__':
#     gunicorn_logger = logging.getLogger('gunicorn.error')
#     flaskapp.logger.handlers = gunicorn_logger.handlers
#     flaskapp.logger.setLevel(gunicorn_logger.level)

def getBookedDays(roomName):
    bookedDays = []
    for booking in mongo.get({'roomName': roomName}):
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
    roomList = []
    for room in mongoRooms.getAll():
        roomList += [room['name']]
    bookingList = []
    for room in roomList:
        booking = Booking(roomId=room, lockDays = mongo.getBookedDays(room))
        # booking = Booking(roomId=room, name=room[0:3], mail=room[0:3]+'@gmail.com', phone='0781828688', lockDays = mongo.getBookedDays(room))
        bookingList += [booking]

    if request.method == "POST":
        print('Form was posted')
        print(request.form)
        # Retrieve the booking by roomId
        for booking in bookingList:
            if booking.roomId == request.form["roomId"]: break
        booking.name = request.form["name"]
        booking.mail = request.form["mail"]
        booking.phone = request.form["phone"]
        booking.startDate = request.form["stayDate"]  # Validate will assign startDate/endDate using it
        booking.yScroll = request.form["yScroll"]  # To keep the scroll position
        if booking.validate():
            registerNewBooking(booking)
            return render_template('confirm.html', booking=booking)
        else:
            print(booking.phone, booking.startDate, booking.endDate)
            return render_template('calendar.html', bookingList=bookingList)
    else: print('Not a post')
    return render_template('calendar.html', bookingList=bookingList)

def registerNewBooking(booking):
        mongo.add({
            'roomName': booking.roomId,
            'startDate': datetime.strptime(booking.startDate, '%Y-%m-%d'),
            'endDate': datetime.strptime(booking.endDate, '%Y-%m-%d'),
            'customerName': booking.name,
            'customerMail': booking.mail,
            'customerPhone': booking.phone
        })
        if flaskapp.config['OS_NAME'] != 'nt':  # Send SMS message only on Linux
        # Send confirmation SMS to us
            msg = 'Réservation du pour La Lande' + booking.startDate + ' au ' + booking.endDate + '\r\n' + \
            'Nom: ' + booking.name + '\r\n' \
            'Phone: ' + booking.phone + '\r\n' \
            'Mail: ' + booking.mail + '\r\n'
            sendSms = SendSms()
            sendSms.sendMessage(msg)
        sendMail = SendMail(booking)

def index_old():
    bookedDays = getBookedDays()
    form = getBookingForm()
    if form.validate_on_submit():
        booking = Booking(form.startDate.data[0:12], form.endDate.data[0:12], "Room to manage later", form.name.data, form.mail.data, form.phone.data)
        return render_template('confirmation.html', booking=booking)
    print(f'index bookedDays={bookedDays}')
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
    roomColor = {'Elodie': '#9090E3', 'Léonie': '#7070E3', 'Mélodie': '#0A0AE3'}
    for bookingRecord in mongo.get({}):  #{'roomName': 'Elodie'}
        booking = Booking(roomId=bookingRecord['roomName'], startDate=bookingRecord['startDate'].strftime('%Y-%m-%d')+'T14:00:00', endDate=bookingRecord['endDate'].strftime('%Y-%m-%d')+'T10:00:00', name=bookingRecord['customerName'], mail=bookingRecord['customerMail'], phone=bookingRecord['customerPhone'], color=roomColor[bookingRecord['roomName']])
        bookingList += [booking]
    # return render_template('bookinglist.html', bookingList=bookingList)
    return render_template('bookingcalendar.html', bookingList=bookingList)

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