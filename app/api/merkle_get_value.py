# from flask_restful import Resource, abort

# from eth_utils import add_0x_prefix

# from app.db import db, Leaf

# from app.util.reqargs import with_args, Argument
# from app.util.types import address


# def parse_data(data):
#     if isinstance(data, str):
#         return int(data, 16)
#     return data


# class MerkleValue(Resource):
#     path = "/merkle/<root_hash>"

#     @with_args(Argument("key", type=address, required=False))
#     def get(self, root_hash, key):
#         db_query = db.session.query(Leaf).filter_by(root_hash=root_hash)
#         if key is not None:
#             db_query = db_query.filter_by(key=add_0x_prefix(key))

#         leaves = db_query.all()
#         return {
#             "result": [
#                 {"key": leaf.key, "value": leaf.value} for leaf in leaves
#             ]
#         }

