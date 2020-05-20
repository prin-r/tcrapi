from flask_restful import Resource, abort

from app.comm.decorators import with_community, with_curve
from app.db import db, Contract
from app.util.abi_data import create_transaction_raw
from app.util.transfer_and_call import create_transfer_and_call
from app.util.reqargs import with_args, Argument
from app.util.types import address


class BuyToken(Resource):
    path = "/dapps/<addr>/buy"

    @with_args(
        Argument("sender", type=address),
        Argument("value", type=int),
        Argument("priceLimit", type=int, dest="price_limit"),
    )
    @with_community(addr="addr")
    @with_curve(addr="addr")
    def post(self, sender, value, price_limit, addr, comm, curve):
        # get band address first
        band_contract = (
            db.session.query(Contract)
            .filter_by(contract_type="BAND_TOKEN")
            .one_or_none()
        ) or abort(400)

        return create_transaction_raw(
            sender,
            band_contract.address,
            create_transfer_and_call(
                sender,
                curve.address,
                price_limit,
                "buy(address,uint256,uint256)",
                ("uint256", value),
            ),
        )
