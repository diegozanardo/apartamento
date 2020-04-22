import pymongo
from bson import ObjectId
from datetime import datetime
import os
import json

class ImageDb():
    credentials = json.loads(os.environ["DATABASE_APARTAMENT"].replace(r"\"", '"'))

    client = pymongo.MongoClient(credentials['server'])
    db = client[credentials['db']]

    collection = db["image"]
    def save(self, image):
        if not '_id' in image:
            print('Inserting')
            self.collection.insert(image)
        else:
            self.collection.update(
                { "_id": ObjectId(image['_id']) }, image)

    def get(self, filter):
        return self.collection.find(filter)

    def get_one(self, filter):
        return self.collection.find_one(filter)


    