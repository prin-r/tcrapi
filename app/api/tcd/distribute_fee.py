from flask_restful import Resource, abort

from app.util.abi_data import create_transaction
from app.util.reqargs import with_args, Argument
from app.util.types import address


class DistributeFee(Resource):
    path = "/data/<addr>/distribute-fee"

    @with_args(Argument("tokenAmount", type=int, dest="token_amount"))
    def post(self, token_amount, addr):
        return create_transaction(
            None, addr, "distributeFee(uint256)", ("uint256", token_amount)
        )

