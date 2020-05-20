import graphene
from sqlalchemy import func
from app.db import db, Transfer as TransferDB
from app.graphql import user as user_module, token as token_module


class UserBalanceFilters(graphene.InputObjectType):
    class Meta:
        description = "Filter for list of user balances, can specify token addresses or user addresses"

    tokens = graphene.List(
        graphene.String,
        description="List of token's ERC-20 addresses to filter",
    )
    users = graphene.List(
        graphene.String,
        description="List of user's Ethereum addresses to filter",
    )


class UserBalance(graphene.ObjectType):
    """ self = Pair of (address of user , CommunityDB Object) """

    class Meta:
        description = "Represents a user's balance of a specific token."

    user = graphene.Field(
        lambda: user_module.User,
        required=True,
        description="The user that owns this user-balance pair.",
    )

    token = graphene.Field(
        lambda: token_module.Token,
        required=True,
        description="The token that this user-balance pair refers to.",
    )

    value = graphene.String(
        required=True,
        description="The balance that this object represents in on-chain unit.",
    )

    def resolve_value(self, info):
        income = (
            db.session.query(func.sum(TransferDB.value))
            .filter_by(receiver=self[0])
            .filter_by(community_id=self[1].id)
            .scalar()
        ) or 0
        expense = (
            db.session.query(func.sum(TransferDB.value))
            .filter_by(sender=self[0])
            .filter_by(community_id=self[1].id)
            .scalar()
        ) or 0
        return str(income - expense)

    def resolve_user(self, info):
        return self[0]

    def resolve_token(self, info):
        return self[1]
