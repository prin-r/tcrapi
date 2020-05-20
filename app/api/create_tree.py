# from flask_restful import Resource, abort

# from app.merkle.smt_call import create_tree

# from app.util.reqargs import with_args, Argument


# def parse_data(data):
#     if isinstance(data, str):
#         return int(data, 16)
#     return data


# class CreateMerkle(Resource):
#     path = "/merkle"

#     @with_args(
#         Argument("keys", type=list, location="json"),
#         Argument("values", type=list, location="json"),
#     )
#     def post(self, keys, values):
#         try:
#             root_hash = create_tree(
#                 [parse_data(key) for key in keys],
#                 [int(value) for value in values],
#             )
#         except Exception as e:
#             abort(400, message=str(e))

#         return {"result": {"rootHash": root_hash}}

