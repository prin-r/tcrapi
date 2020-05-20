import graphene
from sqlalchemy import func
from decimal import Decimal
from datetime import datetime
from app.db import (
    db,
    Poll as PollDB,
    Vote as VoteDB,
    Proposal as ProposalDB,
    Challenge as ChallengeDB,
)

from app.graphql import poll as poll_module


class SimplePoll(graphene.ObjectType):
    """ self = PollDB Object """

    class Meta:
        description = "Represents a poll conducted using BandProtocol's SimpleVoting contract."
        interfaces = (poll_module.Poll,)

    poll_end_time = graphene.DateTime(
        required=True,
        description="The time that this poll will close and stop taking new votes.",
    )

    def resolve_votes(self, info):
        return self.votes

    def resolve_conductor(self, info):
        if self.poll_contract.contract_type == "PARAMETER":
            return (
                db.session.query(ProposalDB)
                .filter_by(
                    community_id=self.poll_contract.community_id,
                    on_chain_id=self.on_chain_id,
                )
                .one()
            )
        elif self.poll_contract.contract_type == "TCR":
            challenges = (
                db.session.query(ChallengeDB)
                .filter_by(
                    contract_id=self.poll_contract.id,
                    on_chain_id=self.on_chain_id,
                )
                .order_by(ChallengeDB.id)
                .all()
            )
            if len(challenges) == 1:
                return (challenges[0], None)
            elif len(challenges) == 2:
                return (challenges[0], challenges[1])
        return None

    def resolve_vote_min_participation(self, info):
        return self.vote_min_participation

    def resolve_vote_support_required(self, info):
        return self.vote_support_required

    def resolve_yes_weight(self, info):
        return (
            db.session.query(func.sum(VoteDB.yes_count))
            .filter_by(poll_id=self.id)
            .scalar()
        ) or Decimal(0)

    def resolve_no_weight(self, info):
        return (
            db.session.query(func.sum(VoteDB.no_count))
            .filter_by(poll_id=self.id)
            .scalar()
        ) or Decimal(0)

    def resolve_status(self, info):
        if (
            datetime.utcnow() < self.reveal_end_time
            or len(self.poll_resolves) == 0
        ):
            return 1
        return int(self.poll_resolves[0].result)

    def resolve_poll_end_time(self, info):
        return self.reveal_end_time
