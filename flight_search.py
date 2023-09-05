import datetime as dt
import requests
from flight_data import FlightData
from pprint import pprint
import os

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = os.environ.get("TKEY")


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.url = "https://api.tequila.kiwi.com/locations/query"
        self.url1 = "https://api.tequila.kiwi.com/v2/search"
        self.header = {
            "apikey": TEQUILA_API_KEY
        }
        self.depart_city = "LON"
        self.currency = "GBP"
        self.tomorrow = dt.datetime.now().date() + dt.timedelta(1)
        self.six_months = dt.datetime.now().date() + dt.timedelta(180)
        self.adult = 1  # can add children, infants
        self.cabin = "M"  # can be M,W,C,F
        self.stops = 0

    def get_destination_code(self, city_name):
        para = {
            "term": city_name,
            "location_types": "city",
        }
        response = requests.get(url=self.url, params=para, headers=self.header)
        response.raise_for_status()
        data = response.json()
        code = data["locations"][0]["code"]
        return code

    def flightcheck(self, destination):
        global flight_data, cityfrom, flyfrom, cityto, flyto, localdeparture, departure, localtime, deptime
        para = {
            "fly_from": self.depart_city,
            "fly_to": destination,
            "date_from": self.tomorrow.strftime("%d/%m/%Y"),
            "date_to": self.six_months.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            # "adults": self.adult,
            # "selected_cabins": self.cabin,
            # "adult_hold_bag": 1,  # for 2 people it is 1,1
            # "adult_hand_bag": 1,  # same as above
            "max_stopovers": self.stops,
            "curr": self.currency
        }
        response = requests.get(url=self.url1, params=para, headers=self.header)
        response.raise_for_status()
        datas = response.json()
        try:
            cheap = datas["data"][0]
        except IndexError as error:
            para["max_stopovers"] = 4
            response = requests.get(url=self.url1, params=para, headers=self.header)
            response.raise_for_status()
            datas = response.json()
            # pprint(datas)
            option = datas["data"][0]
            stops = option['route']
            for i in range(0, len(stops)):
                if i == 0:
                    cityfrom = stops[i]['cityFrom']
                    flyfrom = stops[i]['flyFrom']
                    localdeparture = stops[i]['local_departure'].split('T')[0]
                    localtime = stops[i]["local_departure"].split('T')[1][:-5]
                else:
                    if stops[i]['return'] == 1:
                        cityto = stops[i]['cityFrom']
                        flyto = stops[i]['flyFrom']
                        departure = stops[i]['local_departure'].split('T')[0]
                        deptime = stops[i]["local_departure"].split('T')[1][:-5]
                        break

            stop_travel = [i['cityTo'] for i in stops if i['return'] == 0]
            stop_travel.pop()
            stop_return = [i['cityTo'] for i in stops if i['return'] == 1]
            stop_return.pop()
            stops = [stop_travel, stop_return]
            print(stops)
            flight_data = FlightData(price=option["price"], origin_city=cityfrom,
                                     origin_airport=flyfrom,
                                     destination_city=cityto,
                                     destination_airport=flyto,
                                     out_date=localdeparture,
                                     return_date=departure,
                                     out_time=localtime,
                                     return_time=deptime, via_city=stops)

            # print(f"no flights availaible for {destination}")
            return flight_data
        else:
            flight_data = FlightData(price=cheap["price"], origin_city=cheap['route'][0]["cityFrom"],
                                     origin_airport=cheap["route"][0]["flyFrom"],
                                     destination_city=cheap["route"][0]["cityTo"],
                                     destination_airport=cheap["route"][0]["flyTo"],
                                     out_date=cheap['route'][0]["local_departure"].split('T')[0],
                                     return_date=cheap['route'][1]["local_departure"].split('T')[0],
                                     out_time=cheap['route'][0]["local_departure"].split('T')[1][:-5],
                                     return_time=cheap['route'][1]["local_departure"].split('T')[1][:-5], via_city=[])

            return flight_data
