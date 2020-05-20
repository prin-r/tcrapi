# from flask_restful import Resource, abort

# from eth_utils import add_0x_prefix

# from app.db import db, Leaf

# from app.merkle.smt_call import get_proof

# from app.util.reqargs import with_args, Argument
# from app.util.types import address


# def parse_data(data):
#     if isinstance(data, str):
#         return int(data, 16)
#     return data


# class MerkleProof(Resource):
#     path = "/merkle/<root_hash>/proof/<user>"

#     def get(self, root_hash, user):
#         return {"result": get_proof(user, root_hash)}

