import requests
import json
from datetime import datetime


class TourSearch(object):

    @staticmethod
    def get_reference():
        """возвращает справочник по городам вылета, странам, валютам, классам отелей,
        питанию и типам тура в виде словаря"""
        url = 'https://search.tez-tour.com/tariffsearch/references?locale=ru&formatResult=true&xml=false'
        r = requests.get(url)
        refs = json.loads(r.text)

        cities = {i['name']: i['cityId'] for i in refs['cities']}
        countries = {i['name']: i['countryId'] for i in refs['countries']}
        currencies = {i['name']: i['currencyId'] for i in refs['currencies']}
        hotelClasses = {i['name']: i['classId'] for i in refs['hotelClasses']}
        rAndBs = {i['name']: i['id'] for i in refs['rAndBs']}
        tourTypes = {i['name']: i['id'] for i in refs['tourTypes']}

        return {'cities': cities, 'countries': countries, 'currencies': currencies,
                'hotelClasses': hotelClasses, 'rAndBs': rAndBs, 'tourTypes': tourTypes}

    @staticmethod
    def get_country_reference(country):
        """Возвращает справочник по странам и отелям в каждом регионе в виде словаря"""
        url = f'https://search.tez-tour.com/tariffsearch/byCountry?countryId={country}&cityId=345&locale=ru'
        r = requests.get(url)
        refs = json.loads(r.text)

        tours = {i['name']: 'tourId=' + str(int(str(i['tourId']).lstrip(
            '[').rstrip(']'))) for i in refs['tours']}
        hotels = {i['name']: {'hotelId': i['hotelId'],
                              'tourId': i['tourId']} for i in refs['hotels']}
        regions = {i['name']: i['regionId'] for i in refs['regions']}

        return {'tours': tours, 'hotels': hotels, 'regions': regions}

    @staticmethod
    def get_acc_reference():
        """Возвращает справочник по размещениям в виде словаря"""
        url = f'https://search.tez-tour.com/tariffsearch/getFlightDeparture?cityId=345&countryId=5733&formatResult=true&xml=false'
        r = requests.get(url)
        refs = json.loads(r.text)

        accs = {i['name']: i['accommodationId'] for i in refs['accomodations']}

        return {'accs': accs}

    @staticmethod
    def find_tours(before, after, nightsMin, nightsMax, countryId=1104, tourType=1, cityId=1107, priceMin=0, priceMax=999999,
                   currencyId=8390, accomodationId=2, hotelClassId=2568, hotelClassBetter=True,
                   rAndBId=15350, rAndBBetter=True, tourIds='', noTicketsFrom=False, noTicketsTo=True,
                   hotelInStop=False, promoFlag=True, specialInStop=False):
        url = f'https://search.tez-tour.com/tariffsearch/getResult?priceMin={priceMin}&priceMax={priceMax}&currency={currencyId}&'\
        f'nightsMin={nightsMin}&nightsMax={nightsMax}&hotelClassId={hotelClassId}&accommodationId={accomodationId}&rAndBId={rAndBId}&'\
        f'tourType={tourType}&locale=ru&cityId={cityId}&countryId={countryId}&after={after}&before={before}&'\
        f'{tourIds}&hotelClassBetter={hotelClassBetter}&rAndBBetter={rAndBBetter}&hotelInStop={hotelInStop}&specialInStop={specialInStop}&'\
        f'noTicketsTo={noTicketsTo}&noTicketsFrom={noTicketsFrom}&promoFlag={promoFlag}&version=2&searchTypeId=6&'
        
        r = requests.get(url)
        results = json.loads(r.text)
        return results, url

    def parse_results(self, results):
        hotels = {}
        count = 0
        for i in results['data']:
            startday = ''.join(i[1])
            duration = i[3]
            lastday = i[4]
            region = i[5][0]
            htl_link = i[6][0]
            htl_name = i[6][1]
            htl_image = i[6][2]
            r_and_b = i[7][0]
            randb_full = i[7][1]
            roomtype = i[8][1]
            tourists = i[9][0][0]
            currency = i[10]['currency']
            total = i[10]['total']
            bookit = i[11][0][0]
            comission = i[14]['fixComission']['text']
            cityfrom = i[16][0]
            note = i[18]
            hotels[count] = {'htl_name': htl_name, 'htl_image': htl_image, 'startday': startday, 'duration': duration, 'lastday': lastday, 'region': region, 'htl_link': htl_link, 'randb': r_and_b, 'randbfull': randb_full, 'roomtype': roomtype, 'tourists': tourists, 'currency': currency, 'total': total, 'bookit': bookit, 'comission': comission, 'cityfrom': cityfrom, 'note': note}
            count += 1

        return hotels

# ts = TourSearch()
# ref = ts.get_reference()
# country_ref = ts.get_country_reference(ref['countries']["Турция"])
# print(country_ref['tours'])
# tid_str = ''
# tid_list = []
# for v in TourSearch.get_country_reference(1104)['tours'].values():
#     tid_list = [v for v in TourSearch.get_country_reference(1104)['tours'].values()]
#     tid_str = '&'.join(tid_list)

# print(tid_str)