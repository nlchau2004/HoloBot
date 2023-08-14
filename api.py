import requests
import config


headers = {"X-APIKEY": config.api_key}


def get_streams() -> dict:
    holo_info = requests.get("https://holodex.net/api/v2/live?org=Hololive", headers=headers, timeout=2.5)
    return holo_info.json()


def parse(streams: dict, oshi: list) -> dict:
    oshi_streams = {oshi:{} for oshi in oshi}
    for stream in streams:
        if stream["channel"]["english_name"] in oshi:
            upcoming = {
                "stream": stream["title"],
                "scheduled_time": stream["start_scheduled"],
                "link": stream["channel"]["id"]
                }
            oshi_streams[stream["channel"]["english_name"]].update(upcoming)
    return oshi_streams
