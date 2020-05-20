from flask_restful import Resource, abort
from sqlalchemy import func, desc

from app.comm.decorators import with_tcr
from app.util.eth_call import get_community_token_address
from app.util.reqargs import with_args, Argument
from app.util.abi_data import create_transaction_raw
from app.util.transfer_and_call import create_transfer_and_call
from app.util.types import address
from eth_utils import to_bytes

from datetime import datetime


class TCREntries(Resource):
    path = "/tcr/<addr>/entries"

    @with_args(
        Argument("sender", type=address),
        Argument("dataHash", type=str, dest="data_hash"),
        Argument("deposit", type=int),
    )
    def post(self, addr, sender, data_hash, deposit):
        return create_transaction_raw(
            sender,
            get_community_token_address(addr),
            create_transfer_and_call(
                sender,
                addr,
                deposit,
                "applyEntry(address,uint256,bytes32)",
                ("bytes32", to_bytes(hexstr=data_hash)),
            ),
        )

