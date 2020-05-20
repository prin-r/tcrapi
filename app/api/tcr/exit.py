from flask_restful import Resource

from app.util.reqargs import with_args, Argument
from app.util.abi_data import create_transaction
from app.util.types import address
from eth_utils import to_bytes


class TCRExit(Resource):
    path = "/tcr/<addr>/exit"

    @with_args(
        Argument("sender", type=address),
        Argument("dataHash", type=str, dest="data_hash"),
    )
    def post(self, addr, sender, data_hash):
        return create_transaction(
            sender,
            addr,
            "exit(address,bytes32)",
            ("address", sender),
            ("bytes32", to_bytes(hexstr=data_hash)),
        )

