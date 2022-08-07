import json
import requests
import datetime
import time
import math
import os
from dotenv import load_dotenv

def main():
    with open("settings.json") as file:
        unparsed = file.read()
    
    settings = json.loads(unparsed)

    load_dotenv()

    SLUG = settings["settings.slug"]
    TIME_REFRESH = settings["settings.time.refresh.seconds"]
    TIME_PERIOD = settings["settings.time.period.minutes"]
    PRECENT_INCREASE = settings["settings.trigger.precent.increase"]
    PRECENT_DECREASE = settings["settings.trigger.precent.decrease"]
    WEBHOOK_NEAUTRAL_URL = os.getenv("WEBHOOK_NEATURAL")
    WEBHOOK_INCREASE_URL = os.getenv("WEBHOOK_INCREASE")
    WEBHOOK_DECREASE_URL = os.getenv("WEBHOOK_DECREASE")
    WEBHOOK_NEAUTRAL_NAME = settings["settings.webhooks.neutral.name"]
    WEBHOOK_NEAUTRAL_AVATAR = settings["settings.webhooks.neutral.profile.picture"]
    WEBHOOK_NEAUTRAL_CONTENT = settings["settings.webhooks.neutral.message.content"]
    WEBHOOK_INCREASE_NAME = settings["settings.webhooks.increase.name"]
    WEBHOOK_INCREASE_AVATAR = settings["settings.webhooks.increase.profile.picture"]
    WEBHOOK_INCREASE_CONTENT = settings["settings.webhooks.increase.message.content"]
    WEBHOOK_DECREASE_NAME = settings["settings.webhooks.decrease.name"]
    WEBHOOK_DECREASE_AVATAR = settings["settings.webhooks.decrease.profile.picture"]
    WEBHOOK_DECREASE_CONTENT = settings["settings.webhooks.decrease.message.content"]

    url = f"https://api.opensea.io/api/v1/collection/{SLUG}/stats"

    headers = {"Accept": "application/json"}

    original = ["", ""]
    new = ["", ""]
    total_change = 0
    old_fp = 0
    new_fp = 0

    while True:
        start_time = time.time()
        new_time = start_time

        response = requests.get(url, headers=headers)
        response = json.loads(response.text)

        original[0] = response["stats"]["floor_price"]
        original[1] = f"{datetime.datetime.now().replace(microsecond=0)}"
        old_fp = original[0]

        while new_time - start_time <= (TIME_PERIOD*60):
            response = requests.get(url, headers=headers)
            response = json.loads(response.text)

            new[0] = response["stats"]["floor_price"]
            new[1] = f"{datetime.datetime.now().replace(microsecond=0)}"
            new_fp = new[0]

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
            rate = get_rate("ETH")
            old_usd = old_fp * float(rate)
            new_usd = new_fp * float(rate)

            data = {
                "username": WEBHOOK_DECREASE_NAME,
                "avatar_url": WEBHOOK_DECREASE_AVATAR,
                "content": WEBHOOK_DECREASE_CONTENT,
                "embeds": [
                    {
                        "title": "Floor Price Dropped",
                        "description": f"The floor price has dropped over {PRECENT_DECREASE}% in the past {TIME_PERIOD} minute(s)\n\nDecreasing {round(math.fabs(total_change), 2)}%",
                        "color": 0xF94534,
                        "url": f"https://opensea.io/collection/{SLUG}",
                        "fields": [
                            {
                                "name": "ETH Price",
                                "value": f"Old Floor Price: {round(old_fp, 2)}\nNew Floor Price: {round(new_fp, 2)}",
                                "inline": True
                            }, 
                            {
                                "name": "USD Price",
                                "value": f"Old Floor Price: {round(old_usd, 2)}\nNew Floor Price: {round(new_usd, 2)}",
                                "inline": True
                            }
                        ],
                        "footer": {
                            "text": f"Collection: {SLUG}"
                        }
                    }
                ]
            }

            send_webhook(WEBHOOK_DECREASE_URL, data)
        elif total_change < 0 and math.fabs(total_change) > PRECENT_INCREASE:
            print(f"[INFO] {TIME_PERIOD} mins over")
            print(f"[INFO] precent + change: %{math.fabs(total_change)}")
            rate = get_rate("ETH")
            old_usd = old_fp * float(rate)
            new_usd = new_fp * float(rate)

            data = {
                "username": WEBHOOK_INCREASE_NAME,
                "avatar_url": WEBHOOK_INCREASE_AVATAR,
                "content": WEBHOOK_INCREASE_CONTENT,
                "embeds": [
                    {
                        "title": "Floor Price Increased",
                        "description": f"The floor price has increased over {PRECENT_INCREASE}% in the past {TIME_PERIOD} minute(s)\n\nIncreasing {round(math.fabs(total_change), 2)}%",
                        "color": 0x34F950,
                        "url": f"https://opensea.io/collection/{SLUG}",
                        "fields": [
                            {
                                "name": "ETH Price",
                                "value": f"Old Floor Price: {round(old_fp, 2)}\nNew Floor Price: {round(new_fp, 2)}",
                                "inline": True
                            }, 
                            {
                                "name": "USD Price",
                                "value": f"Old Floor Price: {round(old_usd, 2)}\nNew Floor Price: {round(new_usd, 2)}",
                                "inline": True
                            }
                        ],
                        "footer": {
                            "text": f"Collection: {SLUG}"
                        }
                    }
                ]
            }
            
            send_webhook(WEBHOOK_INCREASE_URL, data)
        else:
            print(f"[INFO] {TIME_PERIOD} mins over")
            print(f"[INFO] No Change")
            rate = get_rate("ETH")
            old_usd = old_fp * float(rate)
            new_usd = new_fp * float(rate)
            data = {
                "username": WEBHOOK_NEAUTRAL_NAME,
                "avatar_url": WEBHOOK_NEAUTRAL_AVATAR,
                "content": WEBHOOK_NEAUTRAL_CONTENT,
                "embeds": [
                    {
                        "title": "Floor Price Stable",
                        "description": f"The floor price has not made enough movement in the past {TIME_PERIOD} minutes.\n\nThe floor price moved {round(math.fabs(total_change), 2)}%",
                        "color": 0x969696,
                        "url": f"https://opensea.io/collection/{SLUG}",
                        "fields": [
                            {
                                "name": "ETH Price",
                                "value": f"Old Floor Price: {round(old_fp, 2)}\nNew Floor Price: {round(new_fp, 2)}",
                                "inline": True
                            }, 
                            {
                                "name": "USD Price",
                                "value": f"Old Floor Price: {round(old_usd, 2)}\nNew Floor Price: {round(new_usd, 2)}",
                                "inline": True
                            }
                        ],
                        "footer": {
                            "text": f"Collection: {SLUG}"
                        }
                    }
                ]
            }

            send_webhook(WEBHOOK_NEAUTRAL_URL, data)

        original = ["", ""]
        new = ["", ""]
        total_change = 0

def get_rate(curency):
    uri = f"https://api.coinbase.com/v2/exchange-rates?currency={curency}"

    response = requests.get(uri)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    
    rates = json.loads(response.text)
    usd_rate = rates["data"]["rates"]["USD"]
    return usd_rate

def send_webhook(url, data):
    res = requests.post(url, json=data)
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print(f"[WEB HOOK] Successfully sent, Code {res.status_code}")
    print("------------")

#def test():

if __name__ == "__main__":
    main()
