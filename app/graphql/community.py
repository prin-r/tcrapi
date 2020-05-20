import graphene
from app.db import db, Contract, Price
from app.graphql import (
    token as token_module,
    order as order_module,
    config as config_module,
    tcr as tcr_module,
    price as price_module,
)
from app.graphql.utils import get_order_history


class Community(graphene.ObjectType):
    """ self = CommunityDB Object """

    class Meta:
        description = "Represents a community in Band Protocol ecosystem, with its own token, configuration, TCRs, etc."

    token = graphene.Field(
        lambda: token_module.Token,
        required=True,
        description="The ERC-20 community token contract object of this community.",
    )

    address = graphene.String(
        required=True,
        description="This community's main contract Ethereum address.",
    )

    order_history = graphene.List(
        lambda: graphene.NonNull(order_module.Order),
        filtered_by=graphene.Argument(lambda: order_module.OrderFilters),
        required=True,
        description="The list of bonding curve orders in this community.",
    )

    price_history = graphene.List(
        lambda: graphene.NonNull(price_module.Price),
        required=True,
        description="The list of spot price updates of this community's token.",
    )

    tcrs = graphene.List(
        lambda: graphene.NonNull(tcr_module.TCR),
        required=True,
        description="The list of Token Curated Registries of this community.",
    )

    config = graphene.Field(
        lambda: config_module.Config,
        required=True,
        description="The configuration contract object of this community.",
    )

    def resolve_token(self, info):
        return self

    def resolve_address(self, info):
        contract = (
            db.session.query(Contract)
            .filter(Contract.community_id == self.id)
            .filter(Contract.contract_type == "CORE")
            .one()
        )
        return contract.address

    def resolve_order_history(self, info, filtered_by={}):
        return get_order_history(**filtered_by, communities=[self])

    def resolve_price_history(self, info):
        return db.session.query(Price).filter_by(community_id=self.id).all()

    def resolve_tcrs(self, info):
        return (
            db.session.query(Contract)
            .filter_by(community_id=self.id, contract_type="TCR")
            .all()
        )

    def resolve_config(self, info):
        return self
