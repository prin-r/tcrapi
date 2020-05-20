import graphene
from sqlalchemy.orm import defer
from app.db import db, Event
from app.graphql import (
    token as token_module,
    user as user_module,
    transaction as transaction_module,
)


class TransferFilters(graphene.InputObjectType):
    class Meta:
        description = "Filter for list of transfers, can specify token addresses or user addresses"

    tokens = graphene.List(
        graphene.String,
        description="List of token's ERC-20 addresses to filter",
    )
    users = graphene.List(
        graphene.String,
        description="List of user's Ethereum addresses to filter",
    )


class Transfer(graphene.ObjectType):
    """ self = TransferDB Object """

    class Meta:
        description = "Represents a transfer event of an ERC-20 token occured in Band Protocol ecosystem."

    token = graphene.Field(
        lambda: token_module.Token,
        required=True,
        description="The token moved with this transfer.",
    )

    sender = graphene.Field(
        lambda: user_module.User,
        required=True,
        description="The sender of this transfer.",
    )

    receiver = graphene.Field(
        lambda: user_module.User,
        required=True,
        description="The receiver of this transfer.",
    )

    value = graphene.String(
        required=True,
        description="The amount of token transfered with this event, in terms of on-chain unit.",
    )

    tx = graphene.Field(
        lambda: transaction_module.Transaction,
        required=True,
        description="The Ethereum transaction that originates this transfer event.",
    )

    def resolve_token(self, info):
        return self.community

    def resolve_sender(self, info):
        return self.sender

    def resolve_receiver(self, info):
        return self.receiver

    def resolve_value(self, info):
        return str(self.value)

    def resolve_tx(self, info):
        return (
            db.session.query(Event)
            .options(defer(Event.data))
            .filter_by(block_id=self.block_id, log_index=self.log_index)
            .one()
        )
