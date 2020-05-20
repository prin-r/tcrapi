# from flask_restful import Resource, abort

# from app.comm.decorators import with_community
# from app.util.abi_data import create_transaction
# from app.util.reqargs import with_args, Argument
# from app.util.types import address

# from eth_utils import remove_0x_prefix


# class SubmitRoot(Resource):
#     path = "/reward/<addr>/add-reward"

#     @with_args(
#         Argument("rootHash", type=str, dest="root_hash"),
#         Argument("totalPortion", type=int, dest="total_portion"),
#     )
#     def post(self, root_hash, total_portion, addr):

#         return create_transaction(
#             None,
#             addr,
#             "addRewardDistribution(bytes32,uint256)",
#             ("bytes32", bytes.fromhex(remove_0x_prefix(root_hash))),
#             ("uint256", total_portion),
#         )
