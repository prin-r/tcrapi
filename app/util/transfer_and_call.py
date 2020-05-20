from eth_utils import function_signature_to_4byte_selector

from app.util.abi_data import create_params_data, create_transaction_data


def create_transfer_and_call(sender, to, value, sig, *params):
    data_to_call = create_params_data(*params)
    return create_transaction_data(
        "transferAndCall(address,address,uint256,bytes4,bytes)",
        ("address", sender),
        ("address", to),
        ("uint256", value),
        ("bytes4", function_signature_to_4byte_selector(sig)),
        ("bytes", data_to_call),
    )
