import requests
from pprint import pprint
import os


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.url = "https://api.sheety.co/356f848b772ab452b535bb902048440a/flightDeals/prices"
        self.user_name = os.environ.get('USER_NAME')
        self.password = os.environ.get('USER_PASSWORD')

    def print(self):
        response = requests.get(url=self.url)
        response.raise_for_status()
        data = response.json()
        # pprint(data['prices'])
        return data['prices']

    def letspost(self, i):
        para = {
            "price": {
                "iataCode": i['iataCode']
            }
        }
        response = requests.put(url=f"{self.url}/{i['id']}", json=para, auth=(self.user_name, self.password))
        response.raise_for_status()
