import graphene
from sqlalchemy.orm import defer
from app.db import db, Event
from app.graphql.transaction import Transaction
from app.graphql import (
    user as user_module,
    community as community_module,
    transaction as transaction_module,
)


class OrderType(graphene.Enum):
    BUY = 1
    SELL = 2


class OrderFilters(graphene.InputObjectType):
    class Meta:
        description = "Filter for list of orders, can specify community addresses, user addresses, order types (buy/sell)"

    order_types = graphene.List(
        OrderType, description="List of order types to filter (buy/sell)"
    )
    communities = graphene.List(
        graphene.String, description="List of community addresses to filter"
    )
    users = graphene.List(
        graphene.String,
        description="List of user's Ethereum addresses to filter",
    )


class Order(graphene.ObjectType):
    """ self = OrderDB Object """

    class Meta:
        description = "Represents a buy or sell order processed by a community's bonding curve."

    user = graphene.Field(
        lambda: user_module.User,
        required=True,
        description="The wallet from which this order transaction is sent.",
    )

    community = graphene.Field(
        lambda: community_module.Community,
        required=True,
        description="The community that this order belongs to.",
    )

    order_type = graphene.Field(
        OrderType,
        required=True,
        description="The type of this order, 'BUY' or 'SELL'",
    )

    value = graphene.String(
        required=True,
        description="The amount of community tokens involved with this order.",
    )

    price = graphene.String(
        required=True,
        description="The amount of BAND tokens involved with this order.",
    )

    commission_cost = graphene.String(
        required=True,
        description="The amount of community tokens taken as order processing fee for the community.",
    )

    tx = graphene.Field(
        lambda: transaction_module.Transaction,
        required=True,
        description="The Ethereum transaction in which this order resides.",
    )

    def resolve_user(self, info):
        return self.user

    def resolve_community(self, info):
        return self.community

    def resolve_order_type(self, info):
        return OrderType[self.order_type.upper()]

    def resolve_value(self, info):
        return str(self.value)

    def resolve_price(self, info):
        return str(self.price)

    def resolve_commission_cost(self, info):
        return str(self.commission_cost)

    def resolve_tx(self, info):
        return (
            db.session.query(Event)
            .options(defer(Event.data))
            .filter_by(block_id=self.block_id, log_index=self.log_index)
            .one()
        )
