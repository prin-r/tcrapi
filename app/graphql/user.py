import graphene
from app.db import (
    db,
    Community as CommunityDB,
    Challenge as ChallengeDB,
    EntryEvent as EntryEventDB,
    Proposal as ProposalDB,
    Entry as EntryDB,
    Vote as VoteDB,
    VoteCommit,
)
from app.graphql.utils import (
    get_order_history,
    get_transfer_history,
    from_address_to_community,
)
from app.graphql import (
    user_balance as user_balance_module,
    transfer as transfer_module,
    order as order_module,
    vote as vote_module,
    proposal as proposal_module,
    reward as reward_module,
    challenge as challenge_module,
    entry as entry_module,
)


class User(graphene.ObjectType):
    """ self = String representing the user's address """

    class Meta:
        description = "Represents an individual's Ethereum wallet that can interact with Band Protocol."

    address = graphene.String(
        required=True, description="The Ethereum address of this user."
    )

    balances = graphene.List(
        lambda: graphene.NonNull(user_balance_module.UserBalance),
        required=True,
        description="The list of token balances that this wallet has.",
        filtered_by=graphene.Argument(
            lambda: user_balance_module.UserBalanceFilters
        ),
    )

    order_history = graphene.List(
        lambda: graphene.NonNull(order_module.Order),
        required=True,
        description="The list of all buy and sell orders conducted by this user to bonding curves.",
        filtered_by=graphene.Argument(lambda: order_module.OrderFilters),
    )
    transfer_history = graphene.List(
        lambda: graphene.NonNull(transfer_module.Transfer),
        required=True,
        description="The list of all transfers sent from or received by this user.",
        filtered_by=graphene.Argument(lambda: transfer_module.TransferFilters),
    )

    proposals = graphene.List(
        lambda: graphene.NonNull(proposal_module.Proposal),
        required=True,
        description="The list of all proposals proposed by this user.",
    )

    votes = graphene.List(
        lambda: graphene.NonNull(vote_module.Vote),
        required=True,
        description="The list of all votes performed by this user.",
        filtered_by=graphene.Argument(lambda: vote_module.VoteFilters),
    )

    tcr_entries = graphene.List(
        lambda: graphene.NonNull(entry_module.Entry),
        required=True,
        description="The list of all TCR entries proposed by this user.",
    )

    tcr_challenges = graphene.List(
        lambda: graphene.NonNull(challenge_module.Challenge),
        required=True,
        description="The list of all TCR challenges initiated by this user.",
    )

    tcr_rewards = graphene.List(
        lambda: graphene.NonNull(reward_module.Reward),
        required=True,
        description="The list of all TCR rewards owned by this user.",
    )

    def resolve_address(self, info):
        return self

    def resolve_balances(self, info, filtered_by={}):
        if "tokens" in filtered_by:
            return [
                (self, comm)
                for comm in from_address_to_community(filtered_by["tokens"])
            ]
        return [(self, comm) for comm in db.session.query(CommunityDB).all()]

    def resolve_order_history(self, info, filtered_by={}):
        if "communities" in filtered_by:
            filtered_by["communities"] = from_address_to_community(
                filtered_by["communities"]
            )
        return get_order_history(**filtered_by, users=[self])

    def resolve_transfer_history(self, info, filtered_by={}):
        if "tokens" in filtered_by:
            filtered_by["tokens"] = from_address_to_community(
                filtered_by["tokens"]
            )
        return get_transfer_history(**filtered_by, users=[self])

    def resolve_votes(self, info, filtered_by={}):
        if "category" in filtered_by and filtered_by["category"] == "cr":
            return [
                (
                    commit_vote,
                    db.session.query(VoteDB)
                    .filter_by(
                        poll_id=commit_vote.poll_id, voter=commit_vote.voter
                    )
                    .first(),
                )
                for commit_vote in db.session.query(VoteCommit)
                .filter_by(voter=self)
                .all()
            ]

        return db.session.query(VoteDB).filter_by(voter=self).all()

    def resolve_proposals(self, info):
        return db.session.query(ProposalDB).filter_by(proposer=self).all()

    def resolve_tcr_rewards(self, info):
        return db.session.query(VoteDB).filter_by(voter=self).all()

    def resolve_tcr_challenges(self, info):
        return [
            (
                challenge_init,
                db.session.query(ChallengeDB)
                .filter_by(contract_id=challenge_init.contract_id)
                .filter_by(on_chain_id=challenge_init.on_chain_id)
                .filter(ChallengeDB.challenger == None)
                .first(),
            )
            for challenge_init in db.session.query(ChallengeDB)
            .filter_by(challenger=self)
            .all()
        ]

    def resolve_tcr_entries(self, info):
        entry_event_ids = [
            entry_event.entry.id
            for entry_event in db.session.query(EntryEventDB)
            .filter_by(actor=self)
            .all()
        ]
        return [
            (
                entry,
                db.session.query(EntryEventDB)
                .filter_by(entry_id=entry.id, action="SUBMITTED")
                .order_by(EntryEventDB.id.desc())
                .first(),
            )
            for entry in db.session.query(EntryDB)
            .filter(EntryDB.id.in_(entry_event_ids))
            .all()
        ]
