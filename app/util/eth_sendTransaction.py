import requests
import os
from eth_utils import is_0x_prefixed, to_checksum_address

BASE_URL = "http://3.81.86.43:"
PORT_SCHEDULER = "8889"
PORT_BODY_GUARD = "8888"


def to_address(data):
    if len(data) != 66 or not is_0x_prefixed(data) or data[2:26] != 24 * "0":
        raise ValueError(f"{data} is not address")
    return to_checksum_address("0x" + data[26:])


def send_scheduler(to, data, when):
    return requests.post(
        BASE_URL + PORT_SCHEDULER + "/schedule",
        json={"to": to, "data": data, "when": when},
    ).json()


def eth_sendTransaction(to, data):
    # send to authen server
    return requests.post(
        BASE_URL + PORT_BODY_GUARD + "/", json={"to": to, "data": data}
    ).json()["result"]
