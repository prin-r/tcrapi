from flask_restful import Resource, abort

from app.comm.decorators import with_poll_contract
from app.util.eth_call import eth_call
from eth_utils import to_bytes
from eth_abi import decode_single

from decimal import Decimal


class TCRMinDeposit(Resource):
    path = "/tcr/<addr>/<entry_hash>/min-deposit"

    @with_poll_contract(addr="addr")
    def get(self, addr, entry_hash, poll_contract):
        min_deposit = Decimal(
            decode_single(
                "uint256",
                to_bytes(
                    hexstr=eth_call(
                        poll_contract.address,
                        "currentMinDeposit(bytes32)",
                        entry_hash,
                    )
                ),
            )
        )

        return {"result": {"minDeposit": min_deposit}}

