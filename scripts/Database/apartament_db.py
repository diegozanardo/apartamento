import pymongo
from bson import ObjectId
from datetime import datetime
import os
import json

class ApartmentDb():
    credentials = json.loads(os.environ["DATABASE_APARTAMENT"].replace(r"\"", '"'))

    client = pymongo.MongoClient(credentials['server'])
    db = client[credentials['db']]

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


    