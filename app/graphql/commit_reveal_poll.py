import graphene
from sqlalchemy import func
from app.db import (
    db,
    Poll as PollDB,
    Vote as VoteDB,
    VoteCommit,
    Proposal as ProposalDB,
    Challenge as ChallengeDB,
)
from app.graphql import poll as poll_module

from decimal import Decimal
from datetime import datetime


class CommitRevealPollStatus(graphene.Enum):
    COMMITTING = 1
    REVEALING = 2
    PENDING_RESOLVE = 3
    RESOLVED = 4


class CommitRevealPoll(graphene.ObjectType):
    """ self = PollDB Object """

    class Meta:
        description = "Represents a poll conducted using BandProtocol's CommitRevealVoting contract."
        interfaces = (poll_module.Poll,)

    current_participation = graphene.String(
        required=True,
        description="The current amount of tokens participated in this poll.",
    )

    commit_end_time = graphene.DateTime(
        required=True,
        description="The time at which this poll stops accepting vote commits.",
    )

    reveal_end_time = graphene.DateTime(
        required=True,
        description="The time at which this poll stops accepting vote reveals.",
    )

    period = graphene.Field(
        CommitRevealPollStatus,
        required=True,
        description="The current status period of this poll.",
    )

    def resolve_votes(self, info, filter_by={}):
        if "voters" in filter_by:
            cr_vote_list = []
            for commit_vote in self.vote_commits:
                if commit_vote.voter in filter_by["voters"]:
                    cr_vote_list.append(
                        (
                            commit_vote,
                            db.session.query(VoteDB)
                            .filter_by(poll_id=self.id, voter=commit_vote.voter)
                            .first(),
                        )
                    )
            return cr_vote_list

        return [
            (
                commit_vote,
                db.session.query(VoteDB)
                .filter_by(poll_id=self.id, voter=commit_vote.voter)
                .first(),
            )
            for commit_vote in self.vote_commits
        ]

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

    def resolve_period(self, info):
        if len(self.poll_resolves) > 0:
            return CommitRevealPollStatus.RESOLVED
        if datetime.utcnow() < self.commit_end_time:
            return CommitRevealPollStatus.COMMITTING
        if datetime.utcnow() < self.reveal_end_time:
            return CommitRevealPollStatus.REVEALING
        return CommitRevealPollStatus.PENDING_RESOLVE

    def resolve_status(self, info):
        if (
            datetime.utcnow() < self.reveal_end_time
            or len(self.poll_resolves) == 0
        ):
            return 1
        return int(self.poll_resolves[0].result)

    def resolve_current_participation(self, info):
        return (
            db.session.query(func.sum(VoteCommit.total_weight))
            .filter_by(poll_id=self.id)
            .scalar()
        ) or Decimal(0)

    def resolve_commit_end_time(self, info):
        return self.commit_end_time

    def resolve_reveal_end_time(self, info):
        return self.reveal_end_time
