import requests
import config

headers = {"X-APIKEY": config.api_key}

r = requests.get("https://holodex.net/api/v2/live?org=Hololive", headers=headers)
for stream in r.json():
    print(stream)
