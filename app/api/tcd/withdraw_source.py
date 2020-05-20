from flask_restful import Resource, abort

from app.util.abi_data import create_transaction
from app.util.reqargs import with_args, Argument
from app.util.types import address


class WithdrawSource(Resource):
    path = "/data/<addr>/withdraw"

    @with_args(
        Argument("sender", type=address),
        Argument("withdrawOwnership", type=int, dest="withdraw_ownership"),
        Argument("dataSource", type=address, dest="data_source"),
    )
    def post(self, sender, withdraw_ownership, data_source, addr):
        return create_transaction(
            sender,
            addr,
            "withdraw(address,uint256,address)",
            ("address", sender),
            ("uint256", withdraw_ownership),
            ("address", data_source),
        )

