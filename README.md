# Floor Price Alerts

This is a simple program made in python to send a message every time the floor price goes over x% in y amount of time, or drops x% in y amount of time.

## How to use
The first thing you will want to do is create a `.env` file in the directory you will be running the file in

In the `.env` file, fill out the information as follows:
```
WEBHOOK_NEATURAL=<LINK TO WEBHOOK>
WEBHOOK_DECREASE=<LINK TO WEBHOOK>
WEBHOOK_INCREASE=<LINK TO WEBHOOK>
```

Next, open `settings.json` and configure the settings to how you would like.

R = Required    O = Optional

- R `settings.slug` is the ending part of the open sea link, that would be the part after the `...collection/`
- R `settings.curency` is the curency you want to convert the ETH floor price into, it only accepts symobl, for example `USD`. It does suport most regular currencies and most popular crypto currencies
- R `settings.time.refresh.seconds` is the amount of time inbetween requests to get info from the open sea API, it is in seconds
- R `settings.time.period.minutes` is the amount of time the program will run before it posts the webhook, it is in minutes
- R `settings.trigger.price.alert.in.currecy` is the amount of money it has to be below before it will trigger the alert
- R `settings.trigger.price.alert.timeout.in.minutes` is the amount of time in minutes the alert will pause for
- R `settings.trigger.precent.increase` is the precent the floor price needs to increase before it will trigger the increase webhook
- R `settings.trigger.precent.decrease` is the precent the floor price needs to decrease before it will trigger the decrease webhook
- R `settings.webhooks.neutral.enabled` is weather or not it will send the "no change" webhook
- O `settings.webhooks.neutral.name` is the name of the neutral webhook
- O `settings.webhooks.neutral.message.content` is the message that sends with the neutral embed
- O `settings.webhooks.neutral.profile.picture` is a link to the profile picture the neutral webhook should use
- R `settings.webhooks.increase.enabled` is weather or not it will send the increase webhook
- O `settings.webhooks.increase.name` is the name of the increase webhook
- O `settings.webhooks.increase.message.content` is the message that will send with the increase embed
- O `settings.webhooks.increase.profile.picture` is a link to the profile picture the increase webhook should use
- R `settings.webhooks.decrease.enabled` is weather or not it will send the decrease webhook
- O `settings.webhooks.decrease.name` is the name the decrease webhook will use
- O `settings.webhooks.decrease.message.content` is the message that sends with the decrease embed
- O `settings.webhooks.decrease.profile.picture` is a link to the profile picture that the decrease webhook will use 
- O `settings.webhooks.price.alert.name` is the name of the price alert webhook
- O `settings.webhooks.price.alert.message.content` is the message that sends with the price alert
- O `settings.webhooks.price.alert.profile.picture` is a link to the profile picture that the price alert will use

Once you have configured settings.json to your liking, run `main.py`

That is all!

*If you have any questions or suggestions, feel free to dm `Woofer21#0220` on discord!*