import graphene
from sqlalchemy.orm import defer
from app.graphql import (
    user as user_module,
    config as config_module,
    key_value as key_value_module,
    poll as poll_module,
    poll_conductor as poll_conductor_module,
)

from app.db import db, Poll as PollDB, Contract, Event


class Proposal(graphene.ObjectType):
    """ self is Proposal """

    class Meta:
        description = "Represents an on-chain proposal to update the community's configuration parameters."
        interfaces = (poll_conductor_module.PollConductor,)

    proposer = graphene.Field(
        lambda: user_module.User,
        required=True,
        description="The user that proposes this proposal.",
    )

    reason_hash = graphene.String(
        required=True,
        description="IPFS hash of this proposal's reason provided by the proposer.",
    )

    config = graphene.Field(
        lambda: config_module.Config,
        required=True,
        description="The configuration object that this proposal aims to change. ",
    )

    changes = graphene.List(
        lambda: graphene.NonNull(key_value_module.KeyValue),
        required=True,
        description="The list of all key-value changes in this proposal.",
    )

    def resolve_on_chain_id(self, info):
        return self.on_chain_id

    def resolve_poll(self, info):
        parameter_contract_id = (
            db.session.query(Contract.id)
            .filter_by(
                community_id=self.community_id, contract_type="PARAMETER"
            )
            .scalar()
        )
        return (
            db.session.query(PollDB)
            .filter_by(
                poll_contract_id=parameter_contract_id,
                on_chain_id=self.on_chain_id,
            )
            .one()
        )

    def resolve_tx(self, info):
        return (
            db.session.query(Event)
            .options(defer(Event.data))
            .filter_by(block_id=self.block_id, log_index=self.log_index)
            .one()
        )

    def resolve_proposer(self, info):
        return self.proposer

    def resolve_reason_hash(self, info):
        return self.reason_hash

    def resolve_config(self, info):
        return self.community

    def resolve_changes(self, info):
        return [
            (parameter.key, parameter.value) for parameter in self.parameters
        ]
