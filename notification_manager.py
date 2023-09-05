import smtplib
import requests
import os


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.email = os.environ.get('TESTMAIL')
        self.password = os.environ.get('TESTPASSWORD')
        self.url = "https://api.sheety.co/356f848b772ab452b535bb902048440a/flightDeals/users"

    def send_alert(self, price, origin_city, origin_airport, destination_city, destination_airport,
                   out_date, out_time, return_date, return_time, via_city):
        response = requests.get(url=self.url)
        data = response.json()
        members = data["users"]
        emails = [i["email"] for i in members]
        with smtplib.SMTP("smtp.gmail.com") as connect:
            connect.starttls()
            connect.login(user=self.email, password=self.password)
            if len(via_city) == 0:
                connect.sendmail(from_addr=self.email, to_addrs=emails,
                                 msg=(f"Subject:Cheap flight alert\n\n"
                                      f"Low Price Alert! Only \xA3 {price} to fly from"
                                      f" {origin_city}-{origin_airport} to "
                                      f"{destination_city}-{destination_airport},"
                                      f"from {out_date} at {out_time} to"
                                      f" {return_date} at {return_time}\n"
                                      f"https://www.google.com/travel/flights?q=Flights%20to%20{destination_airport}"
                                      f"%20from%20{origin_airport}%20on%20{out_date}%20through"
                                      f"%20{return_date}").encode('utf-8'))
            else:
                travel_stops = via_city[0]
                return_stops = via_city[1]
                connect.sendmail(from_addr=self.email, to_addrs=emails,
                                 msg=(f"Subject:Cheap flight alert\n\n"
                                      f"Low Price Alert! Only \xA3 {price} to fly from"
                                      f" {origin_city}-{origin_airport} to "
                                      f"{destination_city}-{destination_airport},"
                                      f"from {out_date} at {out_time} to"
                                      f" {return_date} at {return_time}\n"
                                      f"the flight has {len(travel_stops)} stopover from "
                                      f"{origin_city} to {destination_city} via {','.join(travel_stops)} "
                                      f"and has {len(return_stops)} from {destination_city} to {origin_city} "
                                      f"via {','.join(return_stops)}\n"
                                      f"https://www.google.com/travel/flights?q=Flights%20to%20{destination_airport}%20"
                                      f"from%20{origin_airport}%20on%20{out_date}%20through"
                                      f"%20{return_date}").encode('utf-8'))
