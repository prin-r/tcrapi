from flask_restful import Resource, abort
from sqlalchemy import func

from app.comm.decorators import with_community, with_parameter
from app.util.reqargs import with_args, Argument
from app.util.abi_data import create_transaction
from app.util.types import address
from eth_utils import to_bytes

from decimal import Decimal


class ProposeProposal(Resource):
    path = "/parameter/<addr>/propose"

    @with_community(addr="addr")
    @with_parameter(addr="addr")
    @with_args(
        Argument("sender", type=address),
        Argument("reasonHash", type=str, dest="reason_hash"),
        Argument("keys", type=list, location="json"),
        Argument("values", type=list, location="json"),
    )
    def post(self, sender, reason_hash, addr, comm, param, keys, values):
        return create_transaction(
            sender,
            param.address,
            "propose(address,bytes32,bytes32[],uint256[])",
            ("address", sender),
            ("bytes32", to_bytes(hexstr=reason_hash)),
            ("bytes32[]", [bytes(key, "utf-8") for key in keys]),
            ("uint256[]", [int(value, 0) for value in values]),
        )
