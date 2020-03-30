from apartment_service import ApartmentService
from api import Api

if __name__ == '__main__':
    apartment = ApartmentService()
    api = Api()

    apartaments = api.get_vivareal()
    apartment.save(apartaments, "id_vivareal")