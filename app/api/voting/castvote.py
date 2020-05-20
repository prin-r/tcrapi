from flask_restful import Resource, abort

from app.comm.decorators import with_poll_contract
from app.util.reqargs import with_args, Argument
from app.util.abi_data import create_transaction
from app.util.types import address
from app.util.eth_call import get_voting_address


class CastVote(Resource):
    path = "/voting/<addr>/<int:on_chain_id>/castvote"

    @with_poll_contract(addr="addr")
    @with_args(
        Argument("sender", type=address),
        Argument("yesVote", type=int, dest="yes_vote"),
        Argument("noVote", type=int, dest="no_vote"),
    )
    def post(self, addr, sender, yes_vote, no_vote, on_chain_id, poll_contract):
        return create_transaction(
            sender,
            get_voting_address(poll_contract.address),
            "castVote(address,address,uint256,uint256,uint256)",
            ("address", sender),
            ("address", poll_contract.address),
            ("uint256", on_chain_id),
            ("uint256", yes_vote),
            ("uint256", no_vote),
        )
