# from flask_restful import Resource, abort

# from sqlalchemy import func

# from app.comm.decorators import with_community
# from app.util.abi_data import create_transaction
# from app.util.reqargs import with_args, Argument
# from app.util.types import address

# from eth_utils import remove_0x_prefix


# class RewardClaim(Resource):
#     path = "/reward/<addr>/claim"

#     @with_args(
#         Argument("beneficiary", type=address),
#         Argument("rewardPortion", type=int, dest="reward_portion"),
#         Argument("proof", type=list, location="json"),
#         Argument("rewardId", type=int, dest="reward_id"),
#     )
#     def post(self, reward_id, beneficiary, reward_portion, proof, addr):
#         # get band address first
#         return create_transaction(
#             None,
#             addr,
#             "claimReward(address,uint256,uint256,bytes32[])",
#             ("address", beneficiary),
#             ("uint256", int(reward_id)),
#             ("uint256", reward_portion),
#             ("bytes32[]", [bytes.fromhex(remove_0x_prefix(p)) for p in proof]),
#         )
