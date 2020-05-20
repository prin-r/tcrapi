from flask_restful import Resource, abort

from app.util.abi_data import create_transaction
from app.util.reqargs import with_args, Argument
from app.util.types import address


class TCRClaimReward(Resource):
    path = "/tcr/<addr>/claim-reward"

    @with_args(
        Argument("rewardOwner", type=address, dest="reward_owner"),
        Argument("challengeId", type=int, dest="challenge_id"),
    )
    def post(self, addr, reward_owner, challenge_id):
        return create_transaction(
            reward_owner,
            addr,
            "claimReward(address,uint256)",
            ("address", reward_owner),
            ("uint256", challenge_id),
        )
