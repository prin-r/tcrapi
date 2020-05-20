from flask_restful import Resource, abort

from app.util.abi_data import create_transaction
from app.util.reqargs import with_args, Argument
from app.util.types import address

from eth_utils import to_bytes


class GetDataAsNumber(Resource):
    path = "/data/<addr>/get-number"

    @with_args(Argument("key", type=str))
    def post(self, key, addr):
        return create_transaction(
            None, addr, "getAsNumber(bytes32)", ("bytes32", to_bytes(text=key))
        )

