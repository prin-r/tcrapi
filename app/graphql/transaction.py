import graphene


class Transaction(graphene.ObjectType):
    """ self = EventDB Object"""

    class Meta:
        description = "Represents an Ethereum's transaction that is relevant to Band Protocol ecosystem."

    tx_hash = graphene.String(
        required=True, description="The transaction's 32-byte hash."
    )

    block_timestamp = graphene.DateTime(
        required=True, description="The transaction's block timestamp."
    )

    block_height = graphene.Int(
        required=True, description="The transaction's block height."
    )

    def resolve_tx_hash(self, info):
        return self.tx_hash

    def resolve_block_timestamp(self, info):
        return self.block.block_time

    def resolve_block_height(self, info):
        return self.block.id
