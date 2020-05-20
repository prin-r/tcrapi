import graphene
from sqlalchemy.orm import defer
from app.db import db, Event
from app.graphql import transaction as transaction_module, vote as vote_module


class SimpleVote(graphene.ObjectType):
    """ self is Vote Object """

    class Meta:
        description = "Represents a voting action on Band Protocol's SimpleVoting contract."
        interfaces = (vote_module.Vote,)

    tx = graphene.Field(
        lambda: transaction_module.Transaction,
        required=True,
        description="The transaction of this voting action.",
    )

    def resolve_voter(self, info):
        return self.voter

    def resolve_poll(self, info):
        return self.poll

    def resolve_total_weight(self, info):
        return self.yes_count + self.no_count

    def resolve_yes_weight(self, info):
        return self.yes_count

    def resolve_no_weight(self, info):
        return self.no_count

    def resolve_tx(self, info):
        return (
            db.session.query(Event)
            .options(defer(Event.data))
            .filter_by(block_id=self.block_id, log_index=self.log_index)
            .one()
        )
