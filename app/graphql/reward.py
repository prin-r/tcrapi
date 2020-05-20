import graphene
from sqlalchemy import func
from decimal import Decimal
from app.db import (
    db,
    Challenge as ChallengeDB,
    RewardTCRClaim as RewardTCRClaimDB,
    Event as EventDB,
    Vote as VoteDB,
)
from app.graphql import (
    transaction as transaction_module,
    user as user_module,
    challenge as challenge_module,
)


class Reward(graphene.ObjectType):
    """ self is Vote Object """

    class Meta:
        description = "Represents a TCR reward given to a user as participation incentive."

    beneficiary = graphene.Field(
        lambda: user_module.User,
        required=True,
        description="The user that receives tokens from this TCR reward.",
    )

    challenge = graphene.Field(
        lambda: challenge_module.Challenge,
        required=True,
        description="The TCR challenge of this reward.",
    )

    claim_tx = graphene.Field(
        lambda: transaction_module.Transaction,
        description="The transaction sent to claim this reward, if any.",
    )

    reward_value = graphene.String(
        required=True,
        description="The reward amount in terms of community token's on-chain unit.",
    )

    def resolve_beneficiary(self, info):
        return self.voter

    def resolve_challenge(self, info):
        challenges = (
            db.session.query(ChallengeDB)
            .filter_by(
                contract_id=self.poll.poll_contract_id,
                on_chain_id=self.poll.on_chain_id,
            )
            .order_by(ChallengeDB.id)
            .all()
        )
        if len(challenges) == 1:
            return (challenges[0], None)
        elif len(challenges) == 2:
            return (challenges[0], challenges[1])
        return None

    def resolve_claim_tx(self, info):
        claim_obj = (
            db.session.query(RewardTCRClaimDB)
            .filter_by(voter=self.voter)
            .filter_by(poll_id=self.poll_id)
            .one_or_none()
        )
        if claim_obj != None:
            return (
                db.session.query(EventDB)
                .filter_by(log_index=claim_obj.log_index)
                .filter_by(block_id=claim_obj.block_id)
                .one()
            )
        return None

    def resolve_reward_value(self, info):
        challenges = (
            db.session.query(ChallengeDB)
            .filter_by(
                contract_id=self.poll.poll_contract.id,
                on_chain_id=self.poll.on_chain_id,
            )
            .order_by(ChallengeDB.id)
            .all()
        )
        if len(challenges) == 2:
            yes_count = (
                db.session.query(func.sum(VoteDB.yes_count))
                .filter_by(poll_id=self.poll.id)
                .scalar()
            ) or Decimal(0)
            no_count = (
                db.session.query(func.sum(VoteDB.no_count))
                .filter_by(poll_id=self.poll.id)
                .scalar()
            ) or Decimal(0)
            if challenges[1].action == "SUCCESS":
                if yes_count <= 0:
                    return 0
                return (
                    self.yes_count * challenges[1].voter_reward_pool
                ) // yes_count
            elif challenges[1].action == "FAILED":
                if no_count <= 0:
                    return 0
                return (
                    self.no_count * challenges[1].voter_reward_pool
                ) // no_count

        return 0
