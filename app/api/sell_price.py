from flask_restful import Resource

from app.util.eth_call import eth_call
from app.comm.decorators import with_curve

from eth_utils import to_hex, to_bytes
from eth_abi import encode_single, decode_single


class SellPrice(Resource):
    path = "/dapps/<addr>/sell-price/<int:amount>"

    @with_curve(addr="addr")
    def get(self, addr, amount, curve):
        return {
            "result": {
                "amount": str(amount),
                "price": str(
                    decode_single(
                        "uint256",
                        to_bytes(
                            hexstr=eth_call(
                                curve.address,
                                "getSellPrice(uint256)",
                                data=encode_single("uint256", amount),
                            )
                        ),
                    )
                ),
            }
        }
