from flask_restful import Resource, abort

from app.comm.decorators import with_community
from app.db import db, Contract
from app.util.abi_data import create_transaction
from app.util.reqargs import with_args, Argument
from app.util.types import address


class TokenTransfer(Resource):
    path = "/dapps/<addr>/transfer"

    @with_args(
        Argument("sender", type=address),
        Argument("to", type=address),
        Argument("value", type=int),
    )
    @with_community(addr="addr")
    def post(self, sender, to, value, addr, comm):
        token_contract = comm.token_collection[0]
        return create_transaction(
            sender,
            token_contract.address,
            "transferFeeless(address,address,uint256)",
            ("address", sender),
            ("address", to),
            ("uint256", value),
        )
