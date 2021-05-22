# print('mongodb:', __name__)
# if __name__ == "classes.mongodb": from . import config
# else: import config
from pymongo import MongoClient
import pymongo
from datetime import timedelta

class MongoDb:
    def __init__(self, mongoDb, database, collection):
        client = MongoClient(mongoDb)  #tempcollect DB
                
        # Check our DB exists else create it
        self.db = client[database]
        # Check our collection exists else create it
        self.collection = self.db[collection]

    def add(self, record):
        print(record)
        self.collection.insert_one(record)  

    def getAll(self):
        return self.collection.find()
        
    def get(self, filter):
        return self.collection.find(filter).sort('startDate', pymongo.ASCENDING)

    def delete(self):
        self.collection.remove({})

    def getBookedDays(self, roomId):
        bookedDays = []
        for booking in self.collection.find({'roomName': roomId}).sort('startDate', pymongo.ASCENDING):
            # bookedDays += [[booking['startDate'].strftime('%Y-%m-%d'),(booking['endDate'] - timedelta(days=1)).strftime('%Y-%m-%d')]]
            bookedDays += [[booking['startDate'].strftime('%Y-%m-%d'),booking['endDate'].strftime('%Y-%m-%d')]]
            lastDate = booking['endDate']
        print(bookedDays)
        return bookedDays

# Used for testing
# mongo = MongoDb()
# # mongo.add({'city': 'Firbeix', 'temp': 8.1})
# print(mongo.get({'city': 'Firbeix'}))
# for temp in mongo.get({'city': 'Firbeix'}):
#     print(temp['date'], temp['temp'])