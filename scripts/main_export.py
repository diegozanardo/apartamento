from Service.apartment_service import ApartmentService
import io, json
from bson import ObjectId
from bson.json_util import dumps

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

def flattenjson( b, delim ):
    val = {}
    for i in b.keys():
        if isinstance( b[i], dict ):
            get = flattenjson( b[i], delim )
            for j in get.keys():
                val[ i + delim + j ] = get[j]
        elif isinstance( b[i], list):
            s = ''
            for d in b[i]:
                s = s  + str(d) + '; '
            val[i] = s
        else:
            val[i] = b[i]

    return val

if __name__ == '__main__':
    apartmentService = ApartmentService()

    apartaments = apartmentService.get_all()

    if apartaments is None:
        print('Not found')
    else:
        r = []
        for d in apartaments:
            r.append(flattenjson(d, "__"))

        with io.open('data.txt', 'w', encoding='utf-8') as f:

            f.write(json.dumps(r, default=str))
     