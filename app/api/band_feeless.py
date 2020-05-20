from flask_restful import Resource

from app.db import db, Contract
from app.util.abi_data import create_transaction_data
from app.util.reqargs import with_args, Argument
from app.util.types import address
from app.util.eth_sendTransaction import eth_sendTransaction

from eth_utils import remove_0x_prefix


class BandFeeless(Resource):
    path = "/band/feeless"

    @with_args(
        Argument("sender", type=address),
        Argument("to", type=address),
        Argument("newTimestamp", type=int, dest="new_timestamp"),
        Argument("funcInterface", type=str, dest="function_interface"),
        Argument("data", type=str),
        Argument("senderSig", type=str, dest="sender_signature"),
    )
    def post(
        self,
        sender,
        to,
        function_interface,
        new_timestamp,
        data,
        sender_signature,
    ):
        band_factory = (
            db.session.query(Contract)
            .filter_by(contract_type="BAND_FACTORY")
            .first()
        )
        return {
            "result": eth_sendTransaction(
                band_factory.address,
                create_transaction_data(
                    "sendDelegatedExecution(address,address,bytes4,uint256,bytes,bytes)",
                    ("address", sender),
                    ("address", to),
                    (
                        "bytes4",
                        bytes.fromhex(remove_0x_prefix(function_interface)),
                    ),
                    ("uint256", new_timestamp),
                    ("bytes", bytes.fromhex(remove_0x_prefix(data))),
                    (
                        "bytes",
                        bytes.fromhex(remove_0x_prefix(sender_signature)),
                    ),
                ),
            )
        }
