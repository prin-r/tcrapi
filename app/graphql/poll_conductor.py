import graphene
from app.graphql import transaction as transaction_module, poll as poll_module

from app.db import Proposal as ProposalDB


class PollConductor(graphene.Interface):
    """ Abstract class """

    class Meta:
        description = "Represents an object that need to conduct a poll for token holders to determine result."

    on_chain_id = graphene.Int(
        required=True,
        description="The on-chain ID of the poll that this conductor creates.",
    )

    poll = graphene.Field(
        lambda: poll_module.Poll,
        required=True,
        description="The poll object that this conductor creates.",
    )

    tx = graphene.Field(
        lambda: transaction_module.Transaction,
        required=True,
        description="The Ethereum transaction during which this conductor starts its poll.",
    )

    @classmethod
    def resolve_type(cls, instance, info):
        from app.graphql.proposal import Proposal
        from app.graphql.challenge import Challenge

        if isinstance(instance, ProposalDB):
            return Proposal
        return Challenge
