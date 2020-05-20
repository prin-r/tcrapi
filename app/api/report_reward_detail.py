# from flask_restful import Resource, abort

# from app.comm.decorators import with_community
# from app.comm.decorators import with_community
# from app.db import db, Reward
# from app.util.reqargs import with_args, Argument


# class ReportRewardDetail(Resource):
#     path = "/dapps/<addr>/rewards/<int:reward_id>/detail"

#     @with_community(addr="addr")
#     @with_args(
#         Argument("imageLink", type=str, dest="image_link"),
#         Argument("detailLink", type=str, dest="detail_link"),
#         Argument("header", type=str),
#         Argument("period", type=str),
#     )
#     def post(
#         self, reward_id, addr, comm, image_link, detail_link, header, period
#     ):
#         db.session.query(Reward).filter_by(
#             community_id=comm.id, on_chain_id=reward_id
#         ).update(
#             {
#                 "image_link": image_link,
#                 "detail_link": detail_link,
#                 "header": header,
#                 "period": period,
#             }
#         )
#         db.session.commit()

#         return {"result": "OK"}

