from flask_restful import Resource, abort

from app.comm.decorators import with_community, with_curve
from app.db import db, Token
from app.util.transfer_and_call import create_transfer_and_call
from app.util.abi_data import create_transaction_raw
from app.util.reqargs import with_args, Argument
from app.util.types import address


class SellToken(Resource):
    path = "/dapps/<addr>/sell"

    @with_args(
        Argument("sender", type=address),
        Argument("value", type=int),
        Argument("priceLimit", type=int, dest="price_limit"),
    )
    @with_community(addr="addr")
    @with_curve(addr="addr")
    def post(self, sender, value, price_limit, addr, comm, curve):
        # get token address first
        token_contract = comm.token_collection[0]

        return create_transaction_raw(
            sender,
            token_contract.address,
            create_transfer_and_call(
                sender,
                curve.address,
                value,
                "sell(address,uint256,uint256)",
                ("uint256", price_limit),
            ),
        )
