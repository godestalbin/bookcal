import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    WTF_CSRF_ENABLED = False

    # Mongo keys defined at https://cloud.mongodb.com/v2/5fc2042fdc81aa5cf552a7af#clusters
    MONGO_DB = 'mongodb+srv://godestalbin:YK8SfqWUleMufpYz@cluster0.dyrcm.mongodb.net/?retryWrites=true&w=majority'
    DATABASE = 'bookCal'
    COLLECTION = 'bookings'

    # Free mobile data to send SMS
    # https://mobile.free.fr/account/mes-options to get your API key
    FREE_MOBILE_SMS_GATEWAY = [{'userId': '44865512', 'apiKey': 'sNMYTMVy1cTrX4'}, {'userId': '47888331', 'apiKey': '1slDQ4kYKkNFOF'}]