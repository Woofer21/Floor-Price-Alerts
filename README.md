# Floor Price Alerts

This is a simple program made in python to send a message every time the floor price goes over x% in y ammount of time, or drops x% in y ammount of time.

## How to use
The first thing you will want to do is create a `.env` file in the directory you will be running the file in

In the `.env` file, fill out the information as follows:
```
WEBHOOK_NEATURAL=<LINK TO WEBHOOK>
WEBHOOK_DECREASE=<LINK TO WEBHOOK>
WEBHOOK_INCREASE=<LINK TO WEBHOOK>
```

Next, open `settings.json` and configure the settings to how you would like.
- `settings.slug` is the ending part of the open sea link, that would be the part after the `...collection/`
- `settings.curency` is the curency you want to convert the ETH floor price into, it only accepts symobl, for example `USD`. It does suport most regular currencies and most popular crypto currencies
- `settings.time.refresh.seconds` is the ammount of time inbetween requests to get info from the open sea API, it is in seconds
- `settings.time.period.minutes` is the ammount of time the program will run before it posts the webhook, it is in minutes
- `settings.trigger.precent.increase` is the precent the floor price needs to increase before it will trigger the increase webhook
- `settings.trigger.precent.decrease` is the precent the floor price needs to decrease before it will trigger the decrease webhook
- `settings.webhooks.neutral.enabled` is weather or not it will send the "no change" webhook
- `settings.webhooks.neutral.name` is the name of the neutral webhook (optional)
- `settings.webhooks.neutral.message.content` is the message that sends with the neutral embed (optional)
- `settings.webhooks.neutral.profile.picture` is a link to the profile picture the neutral webhook should use (optional)
- `settings.webhooks.increase.enabled` is weather or not it will send the increase webhook
- `settings.webhooks.increase.name` is the name of the increase webhook (optional)
- `settings.webhooks.increase.message.content` is the messgae that will send with the increase embed (optional)
- `settings.webhooks.increase.profile.picture` is a link to the profile picture the increase webhook should use (optional)
- `settings.webhooks.decrease.enabled` is weather or not it will send the decrease webhook
- `settings.webhooks.decrease.name` is the name the decrease webhook will use (optional)
- `settings.webhooks.decrease.message.content` is the messgae that sends with the decrease embed (optional)
- `settings.webhooks.decrease.profile.picture` is a link to the profile picture that the decrease webhook will use (optional)

Once you have configured settings.json to your liking, run `main.py`

That is all!

*If you have any questions or suggestions, feel free to dm `Woofer21#0220` on discord!*