from flask_restful import Resource, abort

from app.db import db, Contract, Proposal, Challenge
from app.comm.decorators import with_poll_contract
from app.util.reqargs import with_args, Argument
from app.util.types import address
from app.util.abi_data import create_params_data
from app.util.eth_call import (
    get_community_token_address,
    get_community_token_address,
    eth_call,
)
from eth_utils import to_hex, to_bytes
from eth_abi import decode_single

from decimal import Decimal


class VotingPower(Resource):
    path = "/voting/<addr>/<int:on_chain_id>/voting-power/<voter>"

    @with_poll_contract(addr="addr")
    def get(self, addr, on_chain_id, voter, poll_contract):
        voting_snapshot = 0
        contract = (
            db.session.query(Contract)
            .filter_by(address=poll_contract.address)
            .one_or_none()
        )

        if contract.contract_type == "TCR":
            challenge = db.session.query(Challenge).filter_by(
                tcr_address=poll_contract.address, challenge_id=on_chain_id
            ).one_or_none() or abort(400, message=f"Challenge not found")
            voting_snapshot = challenge.token_snap_shot
            token_address = get_community_token_address(poll_contract.address)
        elif contract.contract_type == "PARAMETER":
            proposal = db.session.query(Proposal).filter_by(
                parameter_address=poll_contract.address, proposal_id=on_chain_id
            ).one_or_none() or abort(400, message=f"Challenge not found")
            voting_snapshot = proposal.token_snap_shot
            token_address = get_community_token_address(addr)
        else:
            abort(400)

        voting_power = Decimal(
            decode_single(
                "uint256",
                to_bytes(
                    hexstr=eth_call(
                        token_address,
                        "historicalVotingPowerAtNonce(address,uint256)",
                        to_hex(
                            create_params_data(
                                ("address", voter), ("uint256", voting_snapshot)
                            )
                        ),
                    )
                ),
            )
        )
        return {
            "result": {
                "votingPower": voting_power,
                "votingSnapShot": voting_snapshot,
            }
        }

