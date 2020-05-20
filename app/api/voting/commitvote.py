from flask_restful import Resource, abort

from app.comm.decorators import with_poll_contract
from app.util.reqargs import with_args, Argument
from app.util.abi_data import create_transaction
from app.util.types import address
from app.util.eth_call import get_voting_address
from eth_utils import to_bytes


class CommitVote(Resource):
    path = "/voting/<addr>/<int:on_chain_id>/commitvote"

    @with_poll_contract(addr="addr")
    @with_args(
        Argument("sender", type=address),
        Argument("commitHash", type=str, dest="commit_hash"),
        Argument("totalWeight", type=int, dest="total_weight"),
    )
    def post(
        self,
        addr,
        sender,
        commit_hash,
        total_weight,
        on_chain_id,
        poll_contract,
    ):
        return create_transaction(
            sender,
            get_voting_address(poll_contract.address),
            "commitVote(address,address,uint256,bytes32,bytes32,uint256,uint256 )",
            ("address", sender),
            ("address", poll_contract.address),
            ("uint256", on_chain_id),
            ("bytes32", to_bytes(hexstr=commit_hash)),
            ("bytes32", b""),
            ("uint256", total_weight),
            ("uint256", 0),
        )
