from flask_restful import Resource, abort
from sqlalchemy import func

from app.comm.decorators import with_tcr
from app.util.eth_call import get_community_token_address
from app.util.reqargs import with_args, Argument
from app.util.abi_data import create_transaction_raw
from app.util.transfer_and_call import create_transfer_and_call
from app.util.types import address
from eth_utils import to_bytes

from decimal import Decimal
from datetime import datetime


class TCRChallenge(Resource):
    path = "/tcr/<addr>/challenge"

    @with_args(
        Argument("sender", type=address),
        Argument("entryHash", type=str, dest="entry_hash"),
        Argument("amount", type=int),
        Argument("reasonHash", type=str, dest="reason_hash"),
    )
    def post(self, addr, sender, entry_hash, amount, reason_hash):
        return create_transaction_raw(
            sender,
            get_community_token_address(addr),
            create_transfer_and_call(
                sender,
                addr,
                amount,
                "initiateChallenge(address,uint256,bytes32,bytes32)",
                ("bytes32", to_bytes(hexstr=entry_hash)),
                ("bytes32", to_bytes(hexstr=reason_hash)),
            ),
        )

