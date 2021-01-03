import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Mongo keys defined at https://cloud.mongodb.com/v2/5fc2042fdc81aa5cf552a7af#clusters
    MONGO_DB = 'mongodb+srv://godestalbin:YK8SfqWUleMufpYz@cluster0.dyrcm.mongodb.net/?retryWrites=true&w=majority'
    DATABASE = 'bookCal'
    COLLECTION = 'bookings'