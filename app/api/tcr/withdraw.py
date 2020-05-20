from flask_restful import Resource

from app.util.reqargs import with_args, Argument
from app.util.abi_data import create_transaction
from app.util.types import address
from eth_utils import to_bytes


class TCRWithdraw(Resource):
    path = "/tcr/<addr>/withdraw"

    @with_args(
        Argument("sender", type=address),
        Argument("dataHash", type=str, dest="data_hash"),
        Argument("amount", type=int),
    )
    def post(self, addr, sender, data_hash, amount):
        return create_transaction(
            sender,
            addr,
            "withdraw(address,bytes32,uint256)",
            ("address", sender),
            ("bytes32", to_bytes(hexstr=data_hash)),
            ("uint256", amount),
        )

