import graphene
from sqlalchemy import func
from app.db import db, Contract, Transfer as TransferDB
from app.graphql.utils import get_transfer_history
from app.graphql import (
    community as community_module,
    user_balance as user_balance_module,
    transfer as transfer_module,
)


class Token(graphene.ObjectType):
    """ self = CommunityDB Object """

    class Meta:
        description = "Representds an ERC-20 token contract in Band ecosystem, including Band native token and community tokens."

    address = graphene.String(
        required=True, description="This token's ERC-20 address."
    )

    community = graphene.Field(
        lambda: community_module.Community,
        description="The community of this token, in the case of community token.",
    )

    balances = graphene.List(
        lambda: graphene.NonNull(user_balance_module.UserBalance),
        filtered_by=graphene.Argument(
            lambda: user_balance_module.UserBalanceFilters
        ),
        required=True,
        description="The list of user balances of this token.",
    )

    transfer_history = graphene.List(
        lambda: transfer_module.Transfer,
        filtered_by=graphene.Argument(lambda: transfer_module.TransferFilters),
        required=True,
        description="The list of transfers of this token.",
    )

    name = graphene.String(required=True, description="The name of this token.")

    symbol = graphene.String(
        required=True, description="The symbol of this token."
    )

    def resolve_address(self, info):
        contract = (
            db.session.query(Contract)
            .filter(Contract.contract_type == "TOKEN")
            .filter(Contract.community_id == self.id)
            .one()
        )
        return contract.address

    def resolve_community(self, info):
        if self.id == 1:
            return None
        return self

    def resolve_balances(self, info, filtered_by={}):
        if "users" in filtered_by:
            return [(address, self) for address in filtered_by["users"]]
        addresses = (
            db.session.query(func.distinct(TransferDB.receiver))
            .filter(
                TransferDB.receiver
                != "0x0000000000000000000000000000000000000000"
            )
            .filter(TransferDB.community_id == self.id)
            .all()
        )
        return [(address[0], self) for address in addresses]

    def resolve_transfer_history(self, info, filtered_by={}):
        return get_transfer_history(**filtered_by, tokens=[self])

    def resolve_name(self, info):
        return self.name

    def resolve_symbol(self, info):
        return self.symbol
