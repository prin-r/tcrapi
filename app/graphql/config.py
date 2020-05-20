import graphene
from app.db import (
    db,
    Contract,
    Proposal as ProposalDB,
    Parameter as ParameterDB,
)
from app.graphql import (
    proposal as proposal_module,
    config as config_module,
    sub_config as sub_config_module,
    community as community_module,
)


class Config(graphene.ObjectType):
    """ self is Community Object """

    class Meta:
        description = "Represents a community's configuration contract that controls the community's parameters."

    proposals = graphene.List(
        lambda: graphene.NonNull(proposal_module.Proposal),
        required=True,
        description="The list of all proposals for changes in this configuration.",
    )

    sub_configs = graphene.List(
        lambda: graphene.NonNull(sub_config_module.SubConfig),
        required=True,
        description="The list of sub-configurations based on prefix namespace in this configuration contract.",
    )

    community = graphene.Field(
        lambda: community_module.Community,
        required=True,
        description="The community that owns this config contract.",
    )

    address = graphene.String(
        required=True,
        description="The on-chain Ethereum address of this configuration contract.",
    )

    def resolve_proposals(self, info):
        return (
            db.session.query(ProposalDB).filter_by(community_id=self.id).all()
        )

    def resolve_sub_configs(self, info):
        parameters = (
            db.session.query(ParameterDB.key)
            .filter_by(community_id=self.id)
            .all()
        )
        return [
            (self, prefix)
            for prefix in set((param.split(":")[0] for (param,) in parameters))
        ]

    def resolve_community(self, info):
        return self

    def resolve_address(self, info):
        return (
            db.session.query(Contract.address)
            .filter_by(community_id=self.id, contract_type="PARAMETER")
            .scalar()
        )
