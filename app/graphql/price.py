import graphene
from sqlalchemy.orm import defer
from app.db import db, Event
from app.graphql.transaction import Transaction
from app.graphql import transaction as transaction_module


class Price(graphene.ObjectType):
    """ self = PriceDB Object """

    class Meta:
        description = "Represents a community token spot price relative to Band token at a specific time."

    price = graphene.Float(
        required=True,
        description="The spot price of community token, in the unit of BANDs per token.",
    )

    tx = graphene.Field(
        lambda: transaction_module.Transaction,
        required=True,
        description="The transaction that moves the spot price to this price point.",
    )

    def resolve_price(self, info):
        return str(self.price)

    def resolve_tx(self, info):
        return (
            db.session.query(Event)
            .options(defer(Event.data))
            .filter_by(block_id=self.block_id, log_index=self.log_index)
            .one()
        )

