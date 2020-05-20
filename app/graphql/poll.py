import graphene
from app.graphql import (
    poll_conductor as poll_conductor_module,
    vote as vote_module,
)


class PollStatus(graphene.Enum):
    class Meta:
        description = "Status of the poll"

    ACTIVE = 1
    YES = 2
    NO = 3
    INCONCLUSIVE = 4


class Poll(graphene.Interface):
    """ Abstact class """

    class Meta:
        description = "Represents a poll conducted by a Band Protocl's smart contract, regardless of voting implementation details."

    votes = graphene.List(
        lambda: graphene.NonNull(vote_module.Vote),
        required=True,
        description="The list of votes in this poll.",
        filter_by=graphene.Argument(lambda: vote_module.VoteFilters),
    )

    conductor = graphene.Field(
        lambda: poll_conductor_module.PollConductor,
        required=True,
        description="The smart contract that is the conductor of this poll.",
    )

    vote_min_participation = graphene.String(
        required=True,
        description="The minimum voting power count required for this poll to be conclusive.",
    )

    vote_support_required = graphene.String(
        required=True,
        description="The minimum yes vote percentage among the participated votes to conclude the poll as 'YES'.",
    )

    yes_weight = graphene.String(
        description="The current sum of publicly available 'YES' vote count."
    )

    no_weight = graphene.String(
        description="The current sum of publicly available 'NO' vote count."
    )

    status = graphene.Field(
        PollStatus,
        required=True,
        description="The current status of this poll.",
    )

    @classmethod
    def resolve_type(cls, instance, info):
        from app.graphql.simple_poll import SimplePoll
        from app.graphql.commit_reveal_poll import CommitRevealPoll

        if instance.commit_end_time == instance.reveal_end_time:
            return SimplePoll
        return CommitRevealPoll
