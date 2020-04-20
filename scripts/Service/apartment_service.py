from datetime import datetime
import os
from urllib.parse import urlparse
import datetime
from Service.image import Image
from bson import ObjectId
from Database.apartament_db import ApartmentDb

class ApartmentService():
    apartament_db = ApartmentDb()
    img = Image()

    def update_updated(self):
        apartaments = self.get_all()
        for apartment in apartaments:
            self.apartament_db.save(apartment)

    def save(self, documents, id_field):
        count = 0
        for document in documents:
            count += 1
            print('Processing %s/%s' % (count, len(documents)))
            apartment = self.apartament_db.get_one({id_field: document[id_field]})

            if (not apartment):
                self.__create_one(document)
            else:
                self.__update_existing(apartment, document)

    def get_all(self, filter = {}):
        return self.apartament_db.get(filter)

    def add_similares(self, similares, id):
        apartment = self.apartament_db.get_one({'_id': id})
        if (not 'similares' in apartment):
            apartment['similares'] = []

        for similar in similares:
            if not similar in apartment['similares']:
                apartment['similares'].append(similar)

        apartment['similares_updated'] = str(datetime.datetime.now())

        self.apartament_db.save(apartment, False)

    def remove(self, apartment):
        apartment['removed'] = True
        self.apartament_db.save(apartment)

    def __download_images(self, apartment):
        images = []
        for media in apartment['medias']:
            if media['type'] == "IMAGE":
                images.append(self.img.download(media['url']))
        
        apartment['images'] = images

    def __create_one(self, document):
        self.__download_images(document)

        print('Inserting DB')
        self.apartament_db.save(document)

    def __update_existing(self, apartment, document):
        if 'removed' in apartment and apartment['removed']:
            apartment['removed'] = False
        
        apartment = self.__handle_price(apartment, document)

        self.apartament_db.save(apartment)

    def __handle_price(self, apartment, document):
        if (apartment['price'] != document['price']):
            if (not 'price_version' in apartment):
                apartment['price_version'] = []

            apartment['price_version'].append(
                {
                    'price': apartment['price'],
                    'date': str(datetime.datetime.now())
                }
            )
            apartment['price'] = document['price']

        return apartment
