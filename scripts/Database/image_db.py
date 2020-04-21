import pymongo
from bson import ObjectId
from datetime import datetime

class ImageDb():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["apartamentdb"]
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


    