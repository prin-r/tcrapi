from flask_restful import Resource, abort
from app.db import db, Contract
from eth_utils import to_checksum_address

from app.util.reqargs import with_args, Argument
from app.util.types import address

from app.util.abi_data import create_transaction


class CreateTCR(Resource):
    path = "/dapps/<addr>/create-tcr"

    @with_args(
        Argument("prefix", type=str),
        Argument(
            "decayFunction", type=list, location="json", dest="decay_function"
        ),
        Argument("minDeposit", type=int, dest="min_deposit"),
        Argument("applyStageLength", type=int, dest="apply_stage_length"),
        Argument(
            "dispensationPercentage", type=int, dest="dispensation_percentage"
        ),
        Argument("commitTime", type=int, dest="commit_time"),
        Argument("revealTime", type=int, dest="reveal_time"),
        Argument("minParticipationPct", type=int, dest="min_participation_pct"),
        Argument("supportRequiredPct", type=int, dest="support_required_pct"),
    )
    def post(
        self,
        addr,
        prefix,
        decay_function,
        min_deposit,
        apply_stage_length,
        dispensation_percentage,
        commit_time,
        reveal_time,
        min_participation_pct,
        support_required_pct,
    ):
        return create_transaction(
            None,
            addr,
            "createTCR(bytes8,uint256[],uint256,uint256,uint256,uint256,uint256,uint256,uint256)",
            ("bytes8", bytes(prefix, "utf-8")),
            ("uint256[]", [int(token, 0) for token in decay_function]),
            ("uint256", min_deposit),
            ("uint256", apply_stage_length),
            ("uint256", dispensation_percentage),
            ("uint256", commit_time),
            ("uint256", reveal_time),
            ("uint256", min_participation_pct),
            ("uint256", support_required_pct),
        )
