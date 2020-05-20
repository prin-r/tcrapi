# from sqlalchemy import func
# from flask_restful import Resource
# from app.db import db, Community, Price, Transfer, Block

# from decimal import Decimal
# from datetime import datetime, timedelta


# def calculate_supply(comm_id):
#     owner = "0x0000000000000000000000000000000000000000"
#     mint = (
#         db.session.query(func.sum(Transfer.value))
#         .filter_by(community_id=comm_id)
#         .filter_by(sender=owner)
#         .scalar()
#     ) or 0
#     burn = (
#         db.session.query(func.sum(Transfer.value))
#         .filter_by(community_id=comm_id)
#         .filter_by(receiver=owner)
#         .scalar()
#     ) or 0

#     return mint - burn


# def get_current_price(comm_id):
#     price_row = (
#         db.session.query(Price)
#         .filter_by(community_id=comm_id)
#         .order_by(Price.id.desc())
#         .first()
#     )
#     if price_row is None:
#         return None

#     return price_row.price


# def calculate_marketcap(supply, price):
#     if price is None:
#         return Decimal(0)
#     return supply * Decimal(price) / Decimal(1e18)


# def get_price_last_24(comm_id):
#     since = datetime.utcnow() - timedelta(hours=24)
#     price_row = (
#         db.session.query(Price, Block)
#         .filter(Price.community_id == comm_id)
#         .filter(Price.block_id == Block.id)
#         .filter(Block.block_time < since)
#         .order_by(Price.id.desc())
#         .first()
#     )
#     if price_row is None:
#         return None
#     return price_row.Price.price


# def calculate_changed(now_price, old_price):
#     try:
#         if old_price is None or now_price is None:
#             return Decimal(0)
#         return (now_price - old_price) / old_price * 100
#     except:
#         return Decimal(0)


# class Dapps(Resource):
#     path = "/dapps"

#     def get(self):
#         communities = db.session.query(Community).order_by(Community.id).all()
#         dapps = [
#             {
#                 "name": community.name,
#                 "symbol": community.symbol,
#                 "address": [
#                     contract.address
#                     for contract in community.contracts
#                     if contract.contract_type == "CORE"
#                 ][0],
#                 "price": price,
#                 "marketCap": calculate_marketcap(
#                     calculate_supply(community.id), price
#                 ),
#                 "last24Hrs": calculate_changed(
#                     price, get_price_last_24(community.id)
#                 ),
#             }
#             for community in communities[1:]
#             for price in (get_current_price(community.id),)
#         ]
#         return {
#             "result": {
#                 "band": {
#                     "address": [
#                         contract.address
#                         for contract in communities[0].contracts
#                         if contract.contract_type == "TOKEN"
#                     ][0],
#                     "price": Decimal(1.03),
#                     "last24Hrs": Decimal(6.28),
#                 },
#                 "dapps": dapps,
#             }
#         }
