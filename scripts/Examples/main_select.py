from Service.apartment_service import ApartmentService
import json
from bson import ObjectId

vivareal = 'https://www.vivareal.com.br'

def mount_similares(d, keys):
    similares = []
    for similar in d['similares']:
        a = apartmentService.get_all( {'_id': similar} )[0]
        s = convert(a, keys)
        similares.append(s)

    return similares
def convert(d, keys):
    result = {}
    for key in keys:
        vivareal = ''
        place = key.find('.')
        if place != -1:
            second_key = key[place + 1:]
            first_key = key[:place]
            if first_key == 'link':
                vivareal = 'https://www.vivareal.com.br'
            result[key] = vivareal + d.get(first_key).get(second_key)
        else:
            result[key] = d.get(key)
    
    return result

if __name__ == '__main__':
    apartmentService = ApartmentService()

    apartaments = apartmentService.get_all({'id_vivareal': '2464774082'})[0]

    if apartaments is None:
        print('Not found')
    else:
        print(apartaments)
        result = {}
        keys = ['id_vivareal', 'createdAt', 'updatedAt', 'updated', 'address.locationId', 'totalAreas', 'price', 'price_version', 'link.href', 'removed']
        
        result = convert(apartaments, keys)

        result['similares'] = mount_similares(apartaments, keys)

        print(json.dumps(result))
