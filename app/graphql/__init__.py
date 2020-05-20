import graphene
from sqlalchemy import func
from app.db import db, Contract
from app.graphql import (
    user as user_module,
    token as token_module,
    community as community_module,
    tcr as tcr_module,
)
from app.graphql.utils import (
    from_address_to_community,
    get_band_commuinty,
    get_all_communities,
)


class Query(graphene.ObjectType):
    user = graphene.Field(
        lambda: user_module.User,
        address=graphene.String(),
        description="Look up user by Ethereum wallet address.",
    )

    band = graphene.Field(
        lambda: token_module.Token,
        required=True,
        description="Get Band ERC-20 token object",
    )

    token = graphene.Field(
        lambda: token_module.Token,
        address=graphene.String(),
        description="Look up ERC-20 token object by Ethereum contract address.",
    )

    community = graphene.Field(
        lambda: community_module.Community,
        address=graphene.String(),
        description="Look up community object by Ethereum contract address.",
    )

    all_communities = graphene.List(
        lambda: community_module.Community,
        address=graphene.String(),
        description="Get all communities object in Band ecosystem.",
    )

    tcr = graphene.Field(
        lambda: tcr_module.TCR,
        address=graphene.String(),
        description="Look up TCR contract object by Ethereum contract address.",
    )

    def resolve_user(self, info, address):
        return address

    def resolve_band(self, info):
        return get_band_commuinty()

    def resolve_token(self, info, address):
        comm_obj_list = from_address_to_community([address])
        if len(comm_obj_list) > 0:
            return comm_obj_list[0]
        return None

    def resolve_community(self, info, address):
        comm_obj_list = from_address_to_community([address])
        if len(comm_obj_list) > 0:
            return comm_obj_list[0]
        return None

    def resolve_all_communities(self, info):
        return get_all_communities()

    def resolve_tcr(self, info, address):
        return (
            db.session.query(Contract)
            .filter_by(address=address)
            .filter_by(contract_type="TCR")
            .one()
        )


from app.graphql.simple_poll import SimplePoll
from app.graphql.simple_vote import SimpleVote
from app.graphql.commit_reveal_poll import CommitRevealPoll
from app.graphql.commit_reveal_vote import CommitRevealVote

schema = graphene.Schema(
    query=Query,
    types=[SimplePoll, SimpleVote, CommitRevealPoll, CommitRevealVote],
)
