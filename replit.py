import os
import requests

my_secret = os.environ['URL']
my_secret1 = os.environ['USER_NAME']
my_secret2 = os.environ['PASSWORD']

print("Welcome to JaySawt's Flight Club\nWe find find the best flight deals and email you.")
first_name = input("What is your first name?\n")
last_name = input("What is your last name?\n")
email = input("What is your email?\n")
confirm_email = input("Please confirm your email\n")
if email == confirm_email:
    print("Cheers Your are in the flight club")
    para = {
        "user": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
        }
    }

    response = requests.post(url=my_secret, json=para)
    response.raise_for_status()
    print("Success Your email has been added, Looking forward to it")
