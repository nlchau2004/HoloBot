"""
generate.py
This module focuses on generating a json file that contains the channels of hololive members
"""
import json
import requests
import config

headers = {"X-APIKEY": config.API_KEY}

holo1 = requests.get("https://holodex.net/api/v2/channels?org=Hololive&limit=50",
                            headers=headers,
                            timeout=2.5
                        )

holo2 = requests.get("https://holodex.net/api/v2/channels?org=Hololive&offset=50&limit=50",
                            headers=headers,
                            timeout=2.5
                        )

with open("holomem.json", "w") as outfile:
    holomem = holo1.json() + holo2.json()
    json.dump(holomem, outfile)
