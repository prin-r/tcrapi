from flask_restful import Resource, abort

from app.util.abi_data import create_transaction_raw
from app.util.transfer_and_call import create_transfer_and_call
from app.util.reqargs import with_args, Argument
from app.util.types import address
from app.util.eth_call import get_community_token_address


class RegisterSource(Resource):
    path = "/data/<addr>/register"

    @with_args(
        Argument("sender", type=address),
        Argument("stake", type=int),
        Argument("dataSource", type=address, dest="data_source"),
    )
    def post(self, sender, stake, data_source, addr):
        return create_transaction_raw(
            sender,
            get_community_token_address(addr),
            create_transfer_and_call(
                sender,
                addr,
                stake,
                "register(address,uint256,address)",
                ("address", data_source),
            ),
        )

