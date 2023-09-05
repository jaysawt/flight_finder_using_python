#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager


prices = {}
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.print()
for i in sheet_data:
    if i['iataCode'] == "":
        i['iataCode'] = flight_search.get_destination_code(i['city'])
        data_manager.letspost(i)
print(f"sheet_data:\n {sheet_data}")

for city in sheet_data:
    pri = flight_search.flightcheck(city['iataCode'])
    # if pri is None:
    #     continue
    prices[city['city']] = pri.price
    if prices[city['city']] <= city['lowestPrice']:
        notification_manager.send_alert(pri.price, pri.origin_city,
                                        pri.origin_airport, pri.destination_city,
                                        pri.destination_airport, pri.out_date, pri.out_time, pri.return_date,
                                        pri.return_time, pri.via_city)


print(prices)



