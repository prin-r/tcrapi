from eth_utils import to_checksum_address


def address(data):
    if not isinstance(data, str):
        raise ValueError(f"{data} must an address string")
    return to_checksum_address(data)
