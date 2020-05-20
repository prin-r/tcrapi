from flask_restful import Resource, abort

from app.util.abi_data import create_transaction
from app.util.reqargs import with_args, Argument
from app.util.types import address


class KickSource(Resource):
    path = "/data/<addr>/kick"

    @with_args(Argument("dataSource", type=address, dest="data_source"))
    def post(self, data_source, addr):
        return create_transaction(
            None, addr, "kick(address)", ("address", data_source)
        )

