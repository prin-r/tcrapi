import graphene
from app.db import (
    db,
    Entry as EntryDB,
    EntryEvent as EntryEventDB,
    Challenge as ChallengeDB,
)
from app.graphql import (
    entry as entry_module,
    challenge as challenge_module,
    community as community_module,
    sub_config as sub_config_module,
)
from app.util.eth_call import eth_call


class TCR(graphene.ObjectType):
    """ self is TCR Contract Object """

    class Meta:
        description = (
            "Represents a Token Curated Registry contract in a community."
        )

    entries = graphene.List(
        lambda: graphene.NonNull(entry_module.Entry),
        required=True,
        description="The list of all TCR entries that have been proposed to this TCR.",
    )

    challenges = graphene.List(
        lambda: graphene.NonNull(challenge_module.Challenge),
        required=True,
        description="The list of all challenges that have been initiated in this TCR.",
    )

    community = graphene.Field(
        lambda: community_module.Community,
        required=True,
        description="The community object to which this TCR belongs.",
    )

    sub_config = graphene.Field(
        lambda: sub_config_module.SubConfig,
        required=True,
        description="The sub-configuration object that this TCR uses as its parameters.",
    )

    address = graphene.String(
        required=True, description="The on-chain Ethereum address of this TCR."
    )

    def resolve_entries(self, info):
        return [
            (
                entry,
                db.session.query(EntryEventDB)
                .filter_by(entry_id=entry.id, action="SUBMITTED")
                .order_by(EntryEventDB.id.desc())
                .first(),
            )
            for entry in db.session.query(EntryDB)
            .filter_by(contract_id=self.id)
            .all()
        ]

    def resolve_challenges(self, info):
        challenges = (
            db.session.query(ChallengeDB).filter_by(contract_id=self.id).all()
        )
        on_chain_id_to_challenges = {}
        for challenge in challenges:
            on_chain_id = challenge.on_chain_id
            if on_chain_id not in on_chain_id_to_challenges:
                on_chain_id_to_challenges[on_chain_id] = [None, None]
            if challenge.action == "INIT":
                on_chain_id_to_challenges[on_chain_id][0] = challenge
            else:
                on_chain_id_to_challenges[on_chain_id][1] = challenge
        return [tuple(pair) for pair in on_chain_id_to_challenges.values()]

    def resolve_sub_config(self, info):
        prefix = bytearray.fromhex(
            eth_call(self.address, "prefix()")[2:10]
        ).decode()
        return (self.community, prefix)

    def resolve_address(self, info):
        return self.address

