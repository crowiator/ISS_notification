import requests
from datetime import datetime
import smtplib
import time

# Constants
LAT = 36.812370
LNG = 10.093060
MY_EMAIL = "IMPORT_YOUR_MAIL"
PASSWORD = "IMPORT_YOUR_PASSWORD"


# Check if the ISS station is located in your place
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    if LAT - 5 <= iss_latitude <= LAT + 5 and LNG - 5 <= iss_longitude <= LNG + 5:
        return True


# Check if it is a night in your place
def is_night():
    parameters = {
        "lat": LAT,
        "lng": LNG,
        "formatted": 0
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now_hour = datetime.now().hour
    if time_now_hour >= sunset_hour or time_now_hour <= sunrise:
        return True


# Sending email
def main():
    while True:
        time.sleep(60)
        if is_night() and is_iss_overhead():
            email = "pokojnybojovnik22@gmail.com"
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL, to_addrs=email, msg=f"Subject:ISS overhead\n\n HEY YOUU, LOOK INTO SKY!! YOU WILL SEE ISS OVERHEAD ")


# RUN program
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()