"""api.py"""
import requests
import config

headers = {"X-APIKEY": config.API_KEY}


def get_streams() -> dict:
    """
    Retrieves upcoming streams from Hololive members
    Information returned will be contained in json format
    """
    holo_info = requests.get("https://holodex.net/api/v2/live?org=Hololive",
                             headers=headers,
                             timeout=2.5
                             )
    return holo_info.json()


def parse_streams(streams: dict, oshi: list) -> dict:
    """
    Given a json of the streams and list of followed Vtubers,
    this function parses through the information and returns
    a dictionary containing which oshi has an upcoming livestream
    """
    oshi_streams = {oshi:{} for oshi in oshi}
    for stream in streams:
        if stream["channel"]["english_name"] in oshi:
            upcoming = {
                "stream": stream["title"],
                "scheduled_time": stream["start_scheduled"],
                "link": stream["id"],
                "image": stream["channel"]["photo"]
                }
            oshi_streams[stream["channel"]["english_name"]].update(upcoming)
    return oshi_streams
