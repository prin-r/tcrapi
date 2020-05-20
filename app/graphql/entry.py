import graphene
from sqlalchemy.orm import defer
from decimal import Decimal
from datetime import datetime
from app.util.eth_call import eth_call
from eth_utils import to_bytes
from eth_abi import decode_single
from app.db import db, EntryEvent, Event, Challenge as ChallengeDB
from app.graphql import (
    user as user_module,
    challenge as challenge_module,
    entry_history as entry_history_module,
    tcr as tcr_module,
)


class EntryStatus(graphene.Enum):
    APPLIED = 1
    LISTED = 2
    CHALLENGED = 3
    REJECTED = 4
    EXITED = 5


class Entry(graphene.ObjectType):
    """ self is pair of Entry Object and latest submitted entry event """

    class Meta:
        description = (
            "Represents an entry in a Token Curated Registry in a community."
        )

    challenges = graphene.List(
        lambda: graphene.NonNull(challenge_module.Challenge),
        required=True,
        description="The list of all challenges on this TCR entry.",
    )

    latest_challenge = graphene.Field(
        lambda: challenge_module.Challenge,
        description="The latest challenge of this TCR entry. If the entry never got any challenge latest challenge will be null",
    )

    entry_history = graphene.List(
        lambda: graphene.NonNull(entry_history_module.EntryHistory),
        required=True,
        description="The list of all events of this TCR entry.",
    )

    tcr = graphene.Field(
        lambda: tcr_module.TCR,
        required=True,
        description="The Token Curated Registry in which this entry resides.",
    )

    proposer = graphene.Field(
        lambda: user_module.User,
        required=True,
        description="The user that is the proposer of this entry.",
    )

    list_at = graphene.DateTime(
        required=True,
        description="The time at which this entry was/will be listed on the TCR.",
    )

    proposed_at = graphene.DateTime(
        required=True,
        description="The time at which this entry was most recently proposed.",
    )

    current_min_deposit = graphene.String(
        description="The current minimum deposit amount required to keep this entry on the TCR."
    )

    deposit = graphene.String(
        required=True,
        description="The current amount of tokens deposited as stake in this entry.",
    )

    data_hash = graphene.String(
        required=True, description="IPFS hash of this entry's data."
    )

    status = graphene.Field(
        EntryStatus,
        required=True,
        description="The current status of this entry in the TCR.",
    )

    def resolve_challenges(self, info):
        challenges = (
            db.session.query(ChallengeDB)
            .filter_by(entry_id=self[0].id)
            .order_by(ChallengeDB.id)
            .all()
        )
        on_chain_id_to_challenges = {}
        for challenge in challenges:
            on_chain_id = challenge.on_chain_id
            if on_chain_id not in on_chain_id_to_challenges:
                on_chain_id_to_challenges[on_chain_id] = [None, None]
            if challenge.action == "INIT":
                on_chain_id_to_challenges[on_chain_id][0] = challenge
            else:
                on_chain_id_to_challenges[on_chain_id][1] = challenge
        return [tuple(pair) for pair in on_chain_id_to_challenges.values()]

    def resolve_latest_challenge(self, info):
        latest = (
            db.session.query(ChallengeDB)
            .filter_by(entry_id=self[0].id)
            .order_by(ChallengeDB.on_chain_id.desc())
            .limit(2)
            .all()
        )
        if len(latest) == 1:
            return (latest[0], None)
        elif len(latest) == 2:
            if latest[0].action == "INIT":
                return (latest[0], latest[1])
            return (latest[1], latest[0])

        return None

    def resolve_entry_history(self, info):
        history = (
            db.session.query(EntryEvent, Event)
            .options(defer(Event.data))
            .filter(EntryEvent.entry_id == self[0].id)
            .filter(
                (Event.block_id == EntryEvent.block_id)
                & (Event.log_index == EntryEvent.log_index)
            )
            .order_by(EntryEvent.id)
        ).all()
        result = []
        next_list_at = None
        is_challenged = False
        last_challenger = None
        last_proposer = None

        for (entry_event, block_event) in history:
            actor = None
            if entry_event.action == "SUBMITTED":
                actor = entry_event.actor
            elif (
                entry_event.action == "DEPOSITED"
                or entry_event.action == "WITHDRAWN"
            ):
                actor = last_proposer
            elif entry_event.action == "CHALLENGED":
                actor = entry_event.actor
            elif (
                entry_event.action == "KEPT" or entry_event.action == "REJECTED"
            ):
                actor = last_challenger

            # Add event to list
            result.append(
                {
                    "type": entry_event.action,
                    "event": block_event,
                    "deposit_changed": entry_event.deposit_changed,
                    "actor": actor,
                }
            )

            # Check for add LISTED
            if (
                next_list_at is not None
                and not is_challenged
                and entry_event.block.block_time > next_list_at
            ):
                result.append(
                    {
                        "type": "LISTED",
                        "event": None,
                        "deposit_changed": Decimal(0),
                        "actor": None,
                    }
                )
                next_list_at = None

            # Update entry status
            if entry_event.action == "SUBMITTED":
                next_list_at = entry_event.list_at
                is_challenged = False
                last_proposer = entry_event.actor
            elif entry_event.action == "CHALLENGED":
                is_challenged = True
                last_challenger = entry_event.actor
            elif entry_event.action == "EXITED":
                next_list_at = None
                last_proposer = None
            elif entry_event.action == "REJECTED":
                next_list_at = None
                is_challenged = False
                last_challenger = None
            elif entry_event.action == "KEPT":
                if (
                    next_list_at is not None
                    and entry_event.block.block_time > next_list_at
                ):
                    result.append(
                        {
                            "type": "LISTED",
                            "event": None,
                            "deposit_changed": Decimal(0),
                            "actor": None,
                        }
                    )
                    next_list_at = None
                    is_challenged = False
                last_challenger = None

        if next_list_at is not None and datetime.utcnow() > next_list_at:
            result.append(
                {
                    "type": "LISTED",
                    "event": None,
                    "deposit_changed": Decimal(0),
                    "actor": None,
                }
            )
        return list(reversed(result))

    def resolve_tcr(self, info):
        return self[0].contract

    def resolve_proposer(self, info):
        return self[1].actor

    def resolve_list_at(self, info):
        return self[1].list_at

    def resolve_proposed_at(self, info):
        return self[1].block.block_time

    def resolve_current_min_deposit(self, info):
        last_action = (
            db.session.query(EntryEvent.action)
            .filter_by(entry_id=self[0].id)
            .order_by(EntryEvent.id.desc())
            .first()
        )[0]
        if last_action == "EXITED" or last_action == "REJECTED":
            return None
        return Decimal(
            decode_single(
                "uint256",
                to_bytes(
                    hexstr=eth_call(
                        self[0].contract.address,
                        "currentMinDeposit(bytes32)",
                        self[0].data_hash,
                    )
                ),
            )
        )

    def resolve_deposit(self, info):
        return sum(event.deposit_changed for event in self[0].entry_events)

    def resolve_data_hash(self, info):
        return self[0].data_hash

    def resolve_status(self, info):
        last_action = (
            db.session.query(EntryEvent.action)
            .filter_by(entry_id=self[0].id)
            .order_by(EntryEvent.id.desc())
            .first()
        )[0]
        if (
            last_action == "EXITED"
            or last_action == "REJECTED"
            or last_action == "CHALLENGED"
            or last_action == "LISTED"
        ):
            return EntryStatus[last_action]
        else:
            if datetime.utcnow() >= self[1].list_at:
                return EntryStatus["LISTED"]
            else:
                return EntryStatus["APPLIED"]
