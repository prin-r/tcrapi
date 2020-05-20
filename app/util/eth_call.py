import requests
from eth_utils import (
    keccak,
    is_0x_prefixed,
    to_checksum_address,
    function_signature_to_4byte_selector,
    to_bytes,
    to_hex,
)

from eth_abi import decode_abi

BASE_URL = "https://rinkeby.infura.io/v3/d3301689638b40dabad8395bf00d3945"


def to_address(data):
    if len(data) != 66 or not is_0x_prefixed(data) or data[2:26] != 24 * "0":
        raise ValueError(f"{data} is not address")
    return to_checksum_address("0x" + data[26:])


def eth_call(to, sig, data="0x"):
    if not is_0x_prefixed(sig):
        sig = to_hex(function_signature_to_4byte_selector(sig))
    if isinstance(data, bytes):
        data = to_hex(data)
    return requests.post(
        BASE_URL,
        json={
            "jsonrpc": "2.0",
            "method": "eth_call",
            "params": [{"to": to, "data": sig + data[2:]}, "latest"],
            "id": 12,
        },
    ).json()["result"]


def get_band_address(core_address):
    return to_address(eth_call(core_address, "band()"))


def get_community_token_address(core_address):
    return to_address(eth_call(core_address, "token()"))


def get_parameter_address(core_address):
    return to_address(eth_call(core_address, "params()"))


def get_voting_address(param_address):
    return to_address(eth_call(param_address, "voting()"))


def get_token_symbol(token_address):
    return decode_abi(
        ["string"], to_bytes(hexstr=eth_call(token_address, "symbol()"))
    )[0].decode("utf-8")

