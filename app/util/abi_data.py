from eth_utils import (
    to_hex,
    to_bytes,
    function_signature_to_4byte_selector,
    remove_0x_prefix,
    is_0x_prefixed,
)

from eth_abi import encode_single, encode_abi
from app.db import db, DelegatedTransaction
from decimal import Decimal

from sqlalchemy import func


def create_params_data(*params):
    return encode_abi([t[0] for t in params], [t[1] for t in params])


def create_transaction_data(sig, *params):
    if not is_0x_prefixed(sig):
        sig = to_hex(function_signature_to_4byte_selector(sig))

    raw_param = create_params_data(*params)
    return sig + remove_0x_prefix(to_hex(raw_param))


def create_transaction_raw(sender, to, data):
    last_timestamp = None
    if sender != None:
        last_timestamp = (
            db.session.query(DelegatedTransaction.last_timestamp)
            .filter_by(sender=sender)
            .scalar()
            or 0
        )

    return {"result": {"to": to, "lastTimestamp": last_timestamp, "data": data}}


def create_transaction(sender, to, sig, *params):
    return create_transaction_raw(
        sender, to, create_transaction_data(sig, *params)
    )
