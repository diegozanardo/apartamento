from Service.apartment_service import ApartmentService
from Service.api import Api

if __name__ == '__main__':
    apartment = ApartmentService()
    api = Api()

    apartaments = api.get_vivareal()
    apartment.save(apartaments, "id_vivareal")