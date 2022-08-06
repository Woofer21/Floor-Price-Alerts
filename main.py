import json
import requests
import datetime
import time
import math

def main():
    with open("settings.json") as file:
        unparsed = file.read()
    
    settings = json.loads(unparsed)

    SLUG = settings["settings.slug"]
    TIME_REFRESH = settings["settings.time.refresh.seconds"]
    TIME_PERIOD = settings["settings.time.period.minutes"]
    PRECENT_INCREASE = settings["settings.trigger.precent.increase"]
    PRECENT_DECREASE = settings["settings.trigger.precent.decrease"]

    url = f"https://api.opensea.io/api/v1/collection/{SLUG}/stats"

    headers = {"Accept": "application/json"}

    original = ["", ""]
    new = ["", ""]
    total_change = 0

    while True:
        start_time = time.time()
        new_time = start_time

        response = requests.get(url, headers=headers)
        response = json.loads(response.text)

        original[0] = response["stats"]["floor_price"]
        original[1] = f"{datetime.datetime.now().replace(microsecond=0)}"

        while new_time - start_time <= (TIME_PERIOD*60):
            response = requests.get(url, headers=headers)
            response = json.loads(response.text)

            new[0] = response["stats"]["floor_price"]
            new[1] = f"{datetime.datetime.now().replace(microsecond=0)}"

            difference = ((original[0]-new[0])/original[0]) * 100

            total_change += difference
            new_time = time.time()
            if difference != 0.0:
                original[0] = response["stats"]["floor_price"]
                original[1] = f"{datetime.datetime.now().replace(microsecond=0)}"


            print(f"[ORIGINAL] {original}")
            print(f"[NEW] {new}")
            print(f"[DECREESE] {difference}")
            print("------------")

            time.sleep(TIME_REFRESH)

        
        if total_change > 0 and total_change > PRECENT_DECREASE:
            print(f"[INFO] {TIME_PERIOD} mins over")
            print(f"[INFO] precent - change: %{math.fabs(total_change)}")
            print("------------")
        elif total_change < 0 and math.fabs(total_change) > PRECENT_INCREASE:
            print(f"[INFO] {TIME_PERIOD} mins over")
            print(f"[INFO] precent + change: %{math.fabs(total_change)}")
            print("------------")
        original = ["", ""]
        new = ["", ""]
        total_change = 0

if __name__ == "__main__":
    main()
