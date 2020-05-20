import graphene


class KeyValue(graphene.ObjectType):
    """ self is ( key (String), value (String) ) """

    class Meta:
        description = (
            "Represents a key-value pair in a community's configuration."
        )

    key = graphene.String(
        required=True, description="The key name of the configuration."
    )
    value = graphene.String(
        required=True,
        description="The value of the configuration, represented as a 256-bit integer.",
    )

    def resolve_key(self, info):
        return self[0]

    def resolve_value(self, info):
        return self[1]

