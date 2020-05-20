from flask_restful import Resource, abort

from app.db import db, Contract
from app.util.abi_data import create_transaction_data
from app.util.reqargs import with_args, Argument
from app.util.types import address
from app.util.eth_sendTransaction import eth_sendTransaction


class BandRequest(Resource):
    path = "/band/request"

    @with_args(Argument("to", type=address), Argument("value", type=int))
    def post(self, to, value):
        band_contract = (
            db.session.query(Contract)
            .filter_by(contract_type="BAND_TOKEN")
            .one_or_none()
        ) or abort(400)
        return {
            "result": eth_sendTransaction(
                band_contract.address,
                create_transaction_data(
                    "transferFeeless(address,address,uint256)",
                    ("address", "0xDaD2AD37536FB7a44D2C3DaF75E3FdaBAe3d28Be"),
                    ("address", to),
                    ("uint256", value),
                ),
            )
        }
