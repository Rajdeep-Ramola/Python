import os
import requests
#to make authentication
from requests.auth import HTTPBasicAuth
#to load environment variables
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

SHEETY_PRICES_ENDPOINT ="https://api.sheety.co/RDDD/copyOfFlightDeals/prices"


#This class is responsible for interacting the Google Sheet
class DataManager:
    def __init__(self):
        self._user = os.environ["SHEETY_USRERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}

    def get_destination_data(self):
        # Using Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=SHEETY_PRICES_ENDPOINT )
        data = response.json()

        self.destination_data = data["prices"]
        return self.destination_data

#to update google sheets with IATA codes
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)

