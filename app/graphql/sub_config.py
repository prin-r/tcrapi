import graphene
from app.db import db, Parameter as ParameterDB
from app.graphql import config as config_module, key_value as key_value_module


class SubConfig(graphene.ObjectType):
    """ self is (Community Object, Prefix) """

    class Meta:
        description = "Represents a namespace inside a configuration object for a specific prefix."

    main_config = graphene.Field(
        lambda: config_module.Config,
        required=True,
        description="The main config that this sub-config belongs to.",
    )

    prefix = graphene.String(
        required=True, description="The prefix namespace of this sub-config."
    )

    key_values = graphene.List(
        lambda: graphene.NonNull(key_value_module.KeyValue),
        required=True,
        description="The list of currently active key-value pairs that exist in this sub-config.",
    )

    def resolve_main_config(self, info):
        return self[0]

    def resolve_prefix(self, info):
        return self[1]

    def resolve_key_values(self, info):
        return (
            db.session.query(ParameterDB.key, ParameterDB.value)
            .filter_by(status="ACTIVE", community_id=self[0].id)
            .filter(ParameterDB.key.startswith(self[1]))
            .all()
        )
