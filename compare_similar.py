
from apartment_service import ApartmentService
from dateutil.parser import parse
from image import Image

class CompareSimilar:

    __IMAGES_HASH = {}
    __CUTOFF = 5

    __apartament_service = ApartmentService()
    __image_service = Image()

    def __init__(self):
        self.IMAGES_HASH = self.__image_service.get_images_hash()

    def __should_process(self, ap1, ap2):
        if ap1['id_vivareal'] == ap2['id_vivareal']:
            return False

        if not 'similares_updated' in ap1:
            return True
        
        if not 'updated' in ap2:
            return True

        try:
            date1 = parse(ap1['similares_updated'])
            date2 = parse(ap2['updated'])
            return date2 > date1
        except:
            return True

    def __compare_medias(self, medias, medias_compare):
        count_silimiar = 0
        for media in medias:
            for media_compare in medias_compare:
                if media['new_url'] is None or media_compare['new_url'] is None:
                    continue

                img_hash = self.IMAGES_HASH[media['new_url']]
                img_hash_compare = self.IMAGES_HASH[media_compare['new_url']]

                if img_hash - img_hash_compare < self.__CUTOFF:
                    count_silimiar += 1
                    # print('images are similar - %s \n %s' % (media['new_url'], media_compare['new_url']))

        return count_silimiar

    def compare(self):
        apartaments = list(self.__apartament_service.get_all())
        count = 0

        for apartament in apartaments:
            count += 1
            print('Processing Apartament %s/%s' % (count, len(apartaments)))

            for apartament_compare in apartaments:
                if not self.__should_process(apartament, apartament_compare):
                    continue

                similars = []
                qtd_similares = self.__compare_medias(apartament['medias'], apartament_compare['medias'])
            
                if qtd_similares >= 5:
                    print("%s similar with %s (%s photos similars)" % (apartament['id_vivareal'], apartament_compare['id_vivareal'], qtd_similares))
                    similars.append(apartament_compare['_id'])
                
                self.__apartament_service.add_similares(similars, apartament['_id'])
