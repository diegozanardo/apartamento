from apartment_service import ApartmentService
from api import Api

if __name__ == '__main__':
    apartment = ApartmentService()
    api = Api()

    apartaments_api = api.get_vivareal()
    apartments_bd = apartment.get_all()

    for apartment_bd in apartments_bd:
        apartament = next((x for x in apartaments_api if x['id_vivareal'] == apartment_bd['id_vivareal']), None)
        if apartament is None:
            print('Removed - ' + apartment_bd['title'])
            apartment.remove(apartment_bd, True)
    