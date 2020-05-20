from flask_restful import Resource, abort

from app.db import db, Contract
from app.util.abi_data import create_transaction
from app.util.reqargs import with_args, Argument
from app.util.types import address


class BandTransfer(Resource):
    path = "/band/transfer"

    @with_args(
        Argument("sender", type=address),
        Argument("to", type=address),
        Argument("value", type=int),
    )
    def post(self, sender, to, value):
        band_contract = (
            db.session.query(Contract)
            .filter_by(contract_type="BAND_TOKEN")
            .one_or_none()
        ) or abort(400)
        return create_transaction(
            sender,
            band_contract.address,
            "transferFeeless(address,address,uint256)",
            ("address", sender),
            ("address", to),
            ("uint256", value),
        )
