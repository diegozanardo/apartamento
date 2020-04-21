import pymongo
from bson import ObjectId
from datetime import datetime

class ApartmentDb():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["apartamentdb"]
    collection = db["apartment"]

    def save(self, apartment, updated_date = True):
        if not '_id' in apartment:
            self.collection.insert(apartment)
        else:
            if updated_date:
                apartment['updated'] = str(datetime.now())
            self.collection.update(
                { "_id": ObjectId(apartment['_id']) }, apartment)

    def get(self, filter):
        return self.collection.find(filter)

    def get_one(self, filter):
        return self.collection.find_one(filter)


    