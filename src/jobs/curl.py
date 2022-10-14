import json

import requests
from requests.structures import CaseInsensitiveDict


def send_curl(data_dict, route):
    url = f"http://api:8000/{route}"

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    data = json.dumps(data_dict)

    return requests.post(url, headers=headers, data=data)
