import graphene
from sqlalchemy.orm import defer
from app.db import (
    db,
    Poll as PollDB,
    Event as EventDB,
    Vote as VoteDB,
    EntryEvent as EntryEventDB,
)
from app.graphql import (
    poll_conductor as poll_conductor_module,
    user as user_module,
    entry as entry_module,
    reward as reward_module,
)


class ChallengeStatus(graphene.Enum):
    ONGOING = 1
    SUCCESS = 2
    FAILED = 3
    INCONCLUSIVE = 4


class Challenge(graphene.ObjectType):
    """ self is (Challenge Object - Init, Challenge Object - Resolved) """

    class Meta:
        description = (
            "Represents an on-chain TCR challenge for a particular entry."
        )
        interfaces = (poll_conductor_module.PollConductor,)

    rewards = graphene.List(
        lambda: graphene.NonNull(reward_module.Reward),
        required=True,
        description="The rewards of all participants that vote in this challenge.",
    )

    entry = graphene.Field(
        lambda: entry_module.Entry,
        required=True,
        description="The TCR entry of this challenge.",
    )

    challenger = graphene.Field(
        lambda: user_module.User,
        required=True,
        description="The user that initiates this challenge.",
    )

    stake = graphene.String(
        required=True,
        description="The amount of tokens that the challenger submits to initiate this challenge.",
    )

    reward_pool = graphene.String(
        description="The pool of reward tokens to be distributed among the winning voters."
    )

    leader_reward = graphene.String(
        description="The reward tokens that the 'leader' of the challenge's winning side receives."
    )

    reason_hash = graphene.String(
        required=True,
        description="IPFS hash of this challenge's reason provided by the challenger.",
    )

    status = graphene.Field(
        ChallengeStatus,
        required=True,
        description="The status of this challenge.",
    )

    def resolve_rewards(self, info):
        poll = (
            db.session.query(PollDB)
            .filter_by(
                poll_contract_id=self[0].contract_id,
                on_chain_id=self[0].on_chain_id,
            )
            .one()
        )
        return db.session.query(VoteDB).filter_by(poll_id=poll.id).all()

    def resolve_entry(self, info):
        return (
            self[0].entry,
            db.session.query(EntryEventDB)
            .filter_by(entry_id=self[0].entry.id, action="SUBMITTED")
            .order_by(EntryEventDB.id.desc())
            .first(),
        )

    def resolve_challenger(self, info):
        return self[0].challenger

    def resolve_poll(self, info):
        return (
            db.session.query(PollDB)
            .filter_by(
                poll_contract_id=self[0].contract_id,
                on_chain_id=self[0].on_chain_id,
            )
            .one()
        )

    def resolve_tx(self, info):
        return (
            db.session.query(EventDB)
            .options(defer(EventDB.data))
            .filter_by(block_id=self[0].block_id)
            .filter_by(log_index=self[0].log_index)
            .one_or_none()
        )

    def resolve_stake(self, info):
        return self[0].stake

    def resolve_reward_pool(self, info):
        return self[1] and self[1].voter_reward_pool

    def resolve_leader_reward(self, info):
        return self[1] and self[1].leader_reward

    def resolve_reason_hash(self, info):
        return self[0].reason_data

    def resolve_status(self, info):
        if self[1] != None:
            if self[1].action == "SUCCESS":
                return ChallengeStatus.SUCCESS
            elif self[1].action == "FAILED":
                return ChallengeStatus.FAILED
            elif self[1].action == "INCONCLUSIVE":
                return ChallengeStatus.INCONCLUSIVE
        return ChallengeStatus.ONGOING

    def resolve_on_chain_id(self, info):
        return self[0].on_chain_id

