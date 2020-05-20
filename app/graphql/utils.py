import graphene
from app.db import (
    db,
    Order as OrderDB,
    Transfer as TransferDB,
    Community as CommunityDB,
    Contract,
)


def get_order_history(users=None, communities=None, order_types=None):
    query = db.session.query(OrderDB)
    if users is not None:
        query = query.filter(OrderDB.user.in_(users))
    if communities is not None:
        query = query.filter(
            OrderDB.community_id.in_([comm.id for comm in communities])
        )
    if order_types is not None:
        query = query.filter(
            OrderDB.order_type.in_(
                ["BUY" if x == 1 else "SELL" for x in order_types]
            )
        )

    return query.limit(10).all()


def get_transfer_history(users=None, tokens=None):
    query = db.session.query(TransferDB)
    if users is not None:
        query = query.filter(
            (TransferDB.sender.in_(users)) | (TransferDB.receiver.in_(users))
        )
    if tokens is not None:
        query = query.filter(
            TransferDB.community_id.in_([token.id for token in tokens])
        )

    return query.limit(10).all()


def get_all_communities():
    return db.session.query(CommunityDB).filter(CommunityDB.id != 1).all()


def get_band_commuinty():
    return db.session.query(CommunityDB).filter_by(id=1).one()


def from_address_to_community(addresses=None):
    if addresses != None:
        community_ids = [
            contract.community_id
            for contract in (
                db.session.query(Contract)
                .filter(Contract.address.in_(addresses))
                .all()
            )
        ]
        return (
            db.session.query(CommunityDB)
            .filter(CommunityDB.id.in_(community_ids))
            .all()
        )
    return None
