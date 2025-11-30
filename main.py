import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
own_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")
account_sid = "AC70d712aea1d0193bcfbac0d398d735b4"
auth_token = os.environ.get("AUTH_TOKEN")

weather_params = {
    "lat":  43.591290,
    "lon":  -79.650253,
    "appid" : api_key,
    "cnt" : 4
}

response = requests.get(own_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = (response.json())
# id = weather_data["list"][0]["weather"][0]["id"]
will_rain = False

for hour_data in weather_data["list"]:
    condition_code = (hour_data["weather"][0]["id"])
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {"https": os.environ['https_proxy']}
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body = "It's going to rain today. Bring an ☂️",
        from_ = "+18058660449",
        to = "+16478917395"
    )
    print(message.status)