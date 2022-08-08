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

    with open("currencies.json") as file:
        unparsedC = file.read()
    
    currencies = json.loads(unparsedC)

    load_dotenv()

    SLUG = settings["settings.slug"]
    CURRENCY_SYMBOL = settings["settings.currency"]
    CURRENCY_FULL = currencies[settings["settings.currency"]]
    TIME_REFRESH = settings["settings.time.refresh.seconds"]
    TIME_PERIOD = settings["settings.time.period.minutes"]
    PRECENT_INCREASE = settings["settings.trigger.precent.increase"]
    PRECENT_DECREASE = settings["settings.trigger.precent.decrease"]
    PRICE_ALERT_TRIGGER = settings["settings.trigger.price.alert.in.currecy"]
    PRICE_ALERT_TIMEOUT = settings["settings.trigger.price.alert.timeout.in.minutes"]
    WEBHOOK_NEAUTRAL_URL = os.getenv("WEBHOOK_NEATURAL")
    WEBHOOK_INCREASE_URL = os.getenv("WEBHOOK_INCREASE")
    WEBHOOK_DECREASE_URL = os.getenv("WEBHOOK_DECREASE")
    WEBHOOK_PRICE_ALERT_URL = os.getenv("WEBHOOK_PRICE_ALERT")
    WEBHOOK_NEAUTRAL_ENABLED = settings["settings.webhooks.neutral.enabled"]
    WEBHOOK_NEAUTRAL_NAME = settings["settings.webhooks.neutral.name"]
    WEBHOOK_NEAUTRAL_AVATAR = settings["settings.webhooks.neutral.profile.picture"]
    WEBHOOK_NEAUTRAL_CONTENT = settings["settings.webhooks.neutral.message.content"]
    WEBHOOK_INCREASE_ENABLED = settings["settings.webhooks.increase.enabled"]
    WEBHOOK_INCREASE_NAME = settings["settings.webhooks.increase.name"]
    WEBHOOK_INCREASE_AVATAR = settings["settings.webhooks.increase.profile.picture"]
    WEBHOOK_INCREASE_CONTENT = settings["settings.webhooks.increase.message.content"]
    WEBHOOK_DECREASE_ENABLED = settings["settings.webhooks.decrease.enabled"]
    WEBHOOK_DECREASE_NAME = settings["settings.webhooks.decrease.name"]
    WEBHOOK_DECREASE_AVATAR = settings["settings.webhooks.decrease.profile.picture"]
    WEBHOOK_DECREASE_CONTENT = settings["settings.webhooks.decrease.message.content"]
    WEBHOOK_PRICE_ALERT_NAME = settings["settings.webhooks.price.alert.name"]
    WEBHOOK_PRICE_ALERT_AVATAR = settings["settings.webhooks.price.alert.profile.picture"]
    WEBHOOK_PRICE_ALERT_CONTENT = settings["settings.webhooks.price.alert.message.content"]

    url = f"https://api.opensea.io/api/v1/collection/{SLUG}/stats"

    headers = {"Accept": "application/json"}

    original = ["", ""]
    new = ["", ""]
    total_change = 0
    old_fp = 0
    new_fp = 0

    alert_data= {
        "slug": SLUG,
        "alert.price": PRICE_ALERT_TRIGGER,
        "currency.symbol": CURRENCY_SYMBOL,
        "alert.webhook": WEBHOOK_PRICE_ALERT_URL,
        "alert.username": WEBHOOK_PRICE_ALERT_NAME,
        "alert.avatar.url": WEBHOOK_PRICE_ALERT_AVATAR,
        "alert.content": WEBHOOK_PRICE_ALERT_CONTENT,
        "alert.timeout": PRICE_ALERT_TIMEOUT,
        "start.time": time.time()
    }

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

            alrt_price(response["stats"]["floor_price"], alert_data)

            print(f"[ORIGINAL] {original}")
            print(f"[NEW] {new}")
            print(f"[DECREESE] {difference}")
            print("------------")

            time.sleep(TIME_REFRESH)

        
        if total_change > 0 and total_change > PRECENT_DECREASE:
            print(f"[INFO] {TIME_PERIOD} mins over")
            print(f"[INFO] precent - change: %{math.fabs(total_change)}")
            rate = get_rate("ETH", CURRENCY_SYMBOL)
            old_usd = old_fp * float(rate)
            new_usd = new_fp * float(rate)

            data = {
                "username": WEBHOOK_DECREASE_NAME,
                "avatar_url": WEBHOOK_DECREASE_AVATAR,
                "content": WEBHOOK_DECREASE_CONTENT,
                "embeds": [
                    {
                        "title": "Floor Price Dropped",
                        "description": f"The floor price has dropped over {PRECENT_DECREASE}% in the past {TIME_PERIOD} minutes\n\nDecreasing {round(math.fabs(total_change), 2)}%",
                        "color": 0xF94534,
                        "url": f"https://opensea.io/collection/{SLUG}",
                        "fields": [
                            {
                                "name": "ETH Price",
                                "value": f"Old Floor Price: {round(old_fp, 2)}\nNew Floor Price: {round(new_fp, 2)}",
                                "inline": True
                            }, 
                            {
                                "name": f"{CURRENCY_FULL} Price",
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

            if WEBHOOK_DECREASE_ENABLED: send_webhook(WEBHOOK_DECREASE_URL, data)
        elif total_change < 0 and math.fabs(total_change) > PRECENT_INCREASE:
            print(f"[INFO] {TIME_PERIOD} mins over")
            print(f"[INFO] precent + change: %{math.fabs(total_change)}")
            rate = get_rate("ETH", CURRENCY_SYMBOL)
            old_usd = old_fp * float(rate)
            new_usd = new_fp * float(rate)

            data = {
                "username": WEBHOOK_INCREASE_NAME,
                "avatar_url": WEBHOOK_INCREASE_AVATAR,
                "content": WEBHOOK_INCREASE_CONTENT,
                "embeds": [
                    {
                        "title": "Floor Price Increased",
                        "description": f"The floor price has increased over {PRECENT_INCREASE}% in the past {TIME_PERIOD} minutes\n\nIncreasing {round(math.fabs(total_change), 2)}%",
                        "color": 0x34F950,
                        "url": f"https://opensea.io/collection/{SLUG}",
                        "fields": [
                            {
                                "name": "ETH Price",
                                "value": f"Old Floor Price: {round(old_fp, 2)}\nNew Floor Price: {round(new_fp, 2)}",
                                "inline": True
                            }, 
                            {
                                "name": f"{CURRENCY_FULL} Price",
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
            
            if WEBHOOK_INCREASE_ENABLED: send_webhook(WEBHOOK_INCREASE_URL, data)
        else:
            print(f"[INFO] {TIME_PERIOD} mins over")
            print(f"[INFO] No Change")
            rate = get_rate("ETH", CURRENCY_SYMBOL)
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
                                "name": f"{CURRENCY_FULL} Price",
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

            if WEBHOOK_NEAUTRAL_ENABLED: send_webhook(WEBHOOK_NEAUTRAL_URL, data)

        original = ["", ""]
        new = ["", ""]
        total_change = 0

def get_rate(curency, new):
    uri = f"https://api.coinbase.com/v2/exchange-rates?currency={curency}"

    response = requests.get(uri)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    
    rates = json.loads(response.text)
    usd_rate = rates["data"]["rates"][new]
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

def alrt_price(floor_price, alert_data):
    alert_webhook = alert_data["alert.webhook"]
    currency_symbol = alert_data["currency.symbol"]
    alert_price = alert_data["alert.price"]
    slug = alert_data["slug"]
    webhook_name = alert_data["alert.username"]
    webhook_avatar = alert_data["alert.avatar.url"]
    webhook_content = alert_data["alert.content"]
    timeout_time = alert_data["alert.timeout"]
    start_time = alert_data["start.time"]
    new_time = time.time()
    
    rate = get_rate("ETH", currency_symbol)
    converted_price = floor_price * float(rate)

    if round(converted_price, 2) <= round(alert_price, 2):
        if new_time - start_time >= (timeout_time*60):
            alert_data["start.time"] = time.time()
            data = {
                "username": webhook_name,
                "avatar_url": webhook_avatar,
                "content": webhook_content,
                "embeds": [
                    {
                        "title": "Floor Price Low",
                        "description": f"The floor price is below {alert_price} {currency_symbol}\n\nThe current floor price is {round(converted_price, 2)} {currency_symbol} ({round(floor_price, 2)} ETH)\n\n*This message is paused for the next {timeout_time} minutes*",
                        "color": 0xF55B5B,
                        "url": f"https://opensea.io/collection/{slug}",
                        "footer": {
                            "text": f"Collection: {slug}"
                        }
                    }
                ]
            }
            send_webhook(alert_webhook, data)


#def test():

if __name__ == "__main__":
    main()
