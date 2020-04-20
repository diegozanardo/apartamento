import pandas as pd
import numpy as np
from Database.image_db import ImageDb
from Database.apartament_db import ApartmentDb

import imagehash
import PIL


class CompareImageV2():
    apartament_db = ApartmentDb()
    IMGFOLDER = '/home/dzanardo/github/apartamento/images/'
    CUTOFF = 5
    URL_VIVAREAL = 'https://www.vivareal.com.br'

    def read_mongo(self, no_id=True):
        cursor = self.apartament_db.get({})

        df =  pd.DataFrame(list(cursor))
        
        if no_id:
            del df['_id']

        return df
    def haversine_np(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)

        All args must be of equal length.    

        """
        lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

        c = 2 * np.arcsin(np.sqrt(a))
        km = 6367 * c
        return km

    def load_images(self, df_filtered):
        imageDb = ImageDb()
        images = {}

        count = 0
        for index, row in df_filtered.iterrows():
            count += 1
            print('Processing %s/%s' % (count, len(df_filtered)))
            for m in row['images']:
                imgDb = imageDb.get_one({"image": m})
                if imgDb is None:
                    try:
                        file_name = self.IMGFOLDER + m
                        img = PIL.Image.open(file_name)

                        img_hash = imagehash.average_hash(img)
                        images[m] = img_hash
                        newImg = {"image": m, "image_hash": str(img_hash)}
                        imageDb.save(newImg)
                    except:
                        pass
                else:
                    images[imgDb['image']] = imagehash.hex_to_hash(imgDb['image_hash'])

        return images

    def handle_similar(self, df_filtered, item, images):
        for index, row in df_filtered.iterrows():
            count_s = 0
            count_medias = 0
            for m in row['images']:
                print(m)
                if m in images:
                    count_medias += 1
                    for im in item['images'].values[0]:
                        if im in images:           
                            if (images[m] - images[im]) < self.CUTOFF:
                                count_s += 1
                                break
                        
            df_filtered.loc[index,'count_similar'] = count_s
            df_filtered.loc[index,'count_medias'] = count_medias

    def prepare_data(self, df):
        df['point'] = df['address'].apply(lambda v: v.get('point') if isinstance(v, dict) else '')
        df['lon'] = pd.to_numeric(df['point'].apply(lambda v: v.get('lon') if isinstance(v, dict) else ''), errors='coerce')
        df['lat'] = pd.to_numeric(df['point'].apply(lambda v: v.get('lat') if isinstance(v, dict) else ''), errors='coerce')
        df['link_url'] = df['link'].apply(lambda v: v.get('href') if isinstance(v, dict) else '')
        df['link_url'] = self.URL_VIVAREAL + df['link_url']

    def calculate_distance(self, df, lat, log):
        df['dist'] = self.haversine_np(lat, log, df['lat'], df['lon'])

    def get_similares(self, id):
        df = self.read_mongo()
        
        self.prepare_data(df)

        item = df[(df.id_vivareal == '2454100925')]
        self.calculate_distance(df, item['lat'].values[0], item['lon'].values[0])

        df_filtered = df[(df.dist <= 1)].copy()

        images = self.load_images(df_filtered)
        self.handle_similar(df_filtered, item, images)

        df_filtered2 = df_filtered[(df_filtered.count_similar > 1)]
        df_filtered2 = df_filtered2.sort_values(by=['count_similar'], ascending=False)

        cols = ['id_vivareal', 'link_url', 'count_similar', 'count_medias', 'createdAt', 'portal', 
                'updatedAt', 'address', 'totalAreas', 'status', 'price',
                'updated', 'lon', 'lat', 'dist']

        return df_filtered2[(cols)].to_csv('similares.csv', sep=',', encoding='utf-8')
