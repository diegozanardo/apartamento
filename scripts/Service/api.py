import requests

class Api():
    price_from = 400000
    price_to = 750000

    def call_api(self, size, start):
        headers = {
            'authority': 'glue-api.vivareal.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'sec-fetch-dest': 'empty',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
            'x-domain': 'www.vivareal.com.br',
            'origin': 'https://www.vivareal.com.br',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'referer': 'https://www.vivareal.com.br/venda/sp/campinas/apartamento_residencial/com-varanda-gourmet/',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        params = (
            ('addressCity', 'Campinas'),
            ('addressLocationId', 'BR>Sao Paulo>NULL>Campinas'),
            ('addressNeighborhood', ''),
            ('addressState', 'S\xE3o Paulo'),
            ('addressCountry', 'BR'),
            ('addressStreet', ''),
            ('addressZone', ''),
            ('addressPointLat', '-22.909938'),
            ('addressPointLon', '-47.062633'),
            ('amenities', 'GOURMET_BALCONY'),
            ('business', 'SALE'),
            ('facets', 'amenities'),
            ('unitTypes', 'APARTMENT'),
            ('unitSubTypes', 'UnitSubType_NONE,DUPLEX,LOFT,STUDIO,TRIPLEX'),
            ('unitTypesV3', 'APARTMENT'),
            ('usageTypes', 'RESIDENTIAL'),
            ('priceMin', str(self.price_from)),
            ('priceMax', str(self.price_to)),
            ('listingType', 'USED'),
            ('parentId', 'null'),
            ('categoryPage', 'RESULT'),
            ('includeFields', 'page,search,expansion,nearby,fullUriFragments,account,facets,developments'),
            ('size', size),
            ('from', start),
            ('q', ''),
            ('developmentsSize', '5'),
            ('__vt', ''),
        )

        response = requests.get('https://glue-api.vivareal.com/v2/listings', headers=headers, params=params)
        print(response)
            
        while(response.status_code != 200):
            print(response)
            response = requests.get('https://glue-api.vivareal.com/v2/listings', headers=headers, params=params)    
        
        return response.json()

    def get_vivareal(self):
        size = 200
        start = 0
        total = 0
        result = []
        
        while True:
            response = self.call_api(size, start)
            total = response['page']['uriPagination']['total']
            start = start + size
            r = self.convert_apartaments(response['search']['result'])
            result.extend(r)

            if total < (start + size):
                break

        return result
    
    def convert_apartaments(self, apartaments):
        apartaments_final = []
        
        for apartament in apartaments['listings']:
            if(len(apartament['listing']['pricingInfos']) == 1):
                apartament['listing']["price"] = apartament['listing']['pricingInfos'][0]['price']
            else:
                prices_sale = [x for x in apartament['listing']['pricingInfos'] if x['businessType']=='SALE']
                if(len(prices_sale) > 1):
                    print("More than 1 SALE price. Assuming first - " + str(prices_sale))

                apartament['listing']['price'] = prices_sale[0]['price']
            apartament['listing']['id_vivareal'] = apartament['listing']['id']
            del apartament['listing']['id']
            apartament['listing']['medias'] = apartament['medias']
            apartament['listing']['link'] = apartament['link']
            
            apartaments_final.append(apartament['listing'])

        return apartaments_final

        
