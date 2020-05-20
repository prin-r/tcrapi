import graphene
from app.db import db, Event
from sqlalchemy.orm import defer
from app.graphql import transaction as transaction_module, vote as vote_module


class CommitRevealStatus(graphene.Enum):
    COMMITTED = 1
    REVEALED = 2


class CommitRevealVote(graphene.ObjectType):
    """ self is (VoteCommit Object, Vote Object) """

    class Meta:
        description = "Represents a voting action on Band Protocol's CommitRevealVoting contract."
        interfaces = (vote_module.Vote,)

    commit_tx = graphene.Field(
        lambda: transaction_module.Transaction,
        required=True,
        description="The commit transaction of this voting action.",
    )

    reveal_tx = graphene.Field(
        lambda: transaction_module.Transaction,
        description="The reveal transaction of this voting action.",
    )

    commit_hash = graphene.String(
        required=True, description="The commit hash of this voting action"
    )

    status = graphene.Field(
        CommitRevealStatus,
        required=True,
        description="The status of this voting action.",
    )

    def resolve_voter(self, info):
        return self[0].voter

    def resolve_poll(self, info):
        return self[0].poll

    def resolve_total_weight(self, info):
        return self[0].total_weight

    def resolve_yes_weight(self, info):
        return self[1] and self[1].yes_count

    def resolve_no_weight(self, info):
        return self[1] and self[1].no_count

    def resolve_commit_tx(self, info):
        return (
            db.session.query(Event)
            .options(defer(Event.data))
            .filter_by(block_id=self[0].block_id, log_index=self[0].log_index)
            .one()
        )

    def resolve_reveal_tx(self, info):
        return self[1] and (
            db.session.query(Event)
            .options(defer(Event.data))
            .filter_by(block_id=self[1].block_id, log_index=self[1].log_index)
            .one()
        )

    def resolve_commit_hash(self, info):
        return self[0].commit_hash

    def resolve_status(self, info):
        if self[1] is None:
            return 1
        else:
            return 2

