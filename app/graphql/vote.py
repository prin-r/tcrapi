import graphene
from app.graphql import user as user_module, poll as poll_module


class VoteFilters(graphene.InputObjectType):
    class Meta:
        description = "Filter for list of votes, can specify category of vote (simple or cr)"

    category = graphene.String(
        description="Category of vote (default is simple)"
    )

    voters = graphene.List(
        graphene.String, description="Filter list of votes by these voters"
    )


class Vote(graphene.Interface):
    """ Abstract class """

    class Meta:
        description = "Represents a vote action performed by a user, regardless of voting implementation details."

    voter = graphene.Field(
        lambda: user_module.User,
        required=True,
        description="The user that performs for this vote.",
    )

    poll = graphene.Field(
        lambda: poll_module.Poll,
        required=True,
        description="The poll that this vote is casted on.",
    )

    total_weight = graphene.String(
        required=True,
        description="The total token weight that the user commits to this vote.",
    )

    yes_weight = graphene.String(
        description="The current publicly known token weight on the 'YES' side from this vote."
    )

    no_weight = graphene.String(
        description="The current publicly known token weight on the 'NO' side from this vote."
    )

    @classmethod
    def resolve_type(cls, instance, info):
        from app.graphql.simple_vote import SimpleVote
        from app.graphql.commit_reveal_vote import CommitRevealVote

        if isinstance(instance, tuple):
            return CommitRevealVote

        return SimpleVote

