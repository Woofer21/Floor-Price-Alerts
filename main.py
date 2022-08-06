import json
import requests
import datetime
import time

slug = input("Enter Slug: ")

url = f"https://api.opensea.io/api/v1/collection/{slug}/stats"

headers = {"Accept": "application/json"}


def main():
    original = ["", ""]
    new = ["", ""]
    total_change = 0

    while True:
        #start_date = datetime.datetime.now().strftime("%H:%M:%S")
        #run_time = start_date

        start_time = time.time()
        new_time = start_time

        response = requests.get(url, headers=headers)
        response = json.loads(response.text)

        original[0] = response["stats"]["floor_price"]
        original[1] = f"{datetime.datetime.now().replace(microsecond=0)}"

        while new_time - start_time <= 600:
            response = requests.get(url, headers=headers)
            response = json.loads(response.text)

            new[0] = response["stats"]["floor_price"]
            new[1] = f"{datetime.datetime.now().replace(microsecond=0)}"

            decreese = ((original[0]-new[0])/original[0]) * 100

            total_change += decreese
            new_time = time.time()

            print(f"[ORIGINAL] {original}")
            print(f"[NEW] {new}")
            print(f"[DECREESE] {decreese}")
            print("------------")

            time.sleep(30)

            
        print("[INFO] 10 mins over")
        print(f"[INFO] precent change: %{total_change}")
        print("------------")
        original = ["", ""]
        new = ["", ""]
        total_change = 0

main()
