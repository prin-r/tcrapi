from flask_restful import Resource

from app.util.eth_call import get_community_token_address
from app.util.reqargs import with_args, Argument
from app.util.abi_data import create_transaction_raw
from app.util.transfer_and_call import create_transfer_and_call
from app.util.types import address
from eth_utils import to_bytes


class TCRDeposit(Resource):
    path = "/tcr/<addr>/deposit"

    @with_args(
        Argument("sender", type=address),
        Argument("dataHash", type=str, dest="data_hash"),
        Argument("amount", type=int),
    )
    def post(self, addr, sender, data_hash, amount):
        return create_transaction_raw(
            sender,
            get_community_token_address(addr),
            create_transfer_and_call(
                sender,
                addr,
                amount,
                "deposit(address,uint256,bytes32)",
                ("bytes32", to_bytes(hexstr=data_hash)),
            ),
        )

