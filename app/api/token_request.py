from flask_restful import Resource, abort

from app.comm.decorators import with_community
from app.db import db, Contract
from app.util.abi_data import create_transaction_data
from app.util.reqargs import with_args, Argument
from app.util.types import address
from app.util.eth_sendTransaction import eth_sendTransaction
from app.util.transfer_and_call import create_transfer_and_call

from app.api.buy_price import get_buy_price


class TokenRequest(Resource):
    path = "/dapps/<addr>/request"

    @with_args(Argument("to", type=address), Argument("value", type=int))
    @with_community(addr="addr")
    def post(self, addr, comm, to, value):
        token_contract = comm.token_collection[0]
        curve_contract = comm.curve_collection[0]

        request_tx = eth_sendTransaction(
            token_contract.address,
            create_transaction_data(
                "transferFeeless(address,address,uint256)",
                ("address", "0xDaD2AD37536FB7a44D2C3DaF75E3FdaBAe3d28Be"),
                ("address", to),
                ("uint256", value),
            ),
        )

        # get band address
        band_contract = (
            db.session.query(Contract)
            .filter_by(contract_type="BAND_TOKEN")
            .one_or_none()
        ) or abort(400)

        eth_sendTransaction(
            band_contract.address,
            create_transfer_and_call(
                "0xDaD2AD37536FB7a44D2C3DaF75E3FdaBAe3d28Be",
                curve_contract.address,
                int(1.5 * get_buy_price(curve_contract.address, value)),
                "buy(address,uint256,uint256)",
                ("uint256", value),
            ),
        )
        return {"result": request_tx}
