import graphene
from sqlalchemy.orm import defer
from app.db import db
from app.graphql import transaction as transaction_module, user as user_module


class EntryHistoryAction(graphene.Enum):
    SUBMITTED = 1
    LISTED = 2
    CHALLENGED = 3
    DEPOSITED = 4
    WITHDRAWN = 5
    KEPT = 6
    REJECTED = 7
    EXITED = 8


class EntryHistory(graphene.ObjectType):
    """ self is EntryEvent(Custom) Object """

    class Meta:
        description = "Represents an event of a TCR entry."

    proposer = graphene.Field(
        lambda: user_module.User,
        description="The user that introduces this event, or none if not available.",
    )

    tx = graphene.Field(
        lambda: transaction_module.Transaction,
        description="The transaction that originates this event, if any.",
    )

    deposit_changed = graphene.String(
        required=True,
        description="The amount of staked tokens that changed with this event.",
    )

    action = graphene.Field(
        EntryHistoryAction, required=True, description="The event's action."
    )

    def resolve_proposer(self, info):
        return self["actor"]

    def resolve_tx(self, info):
        return self["event"]

    def resolve_deposit_changed(self, info):
        return self["deposit_changed"]

    def resolve_action(self, info):
        return EntryHistoryAction[self["type"]]

