from flask_restful import Resource

from app.util.eth_call import eth_call
from app.comm.decorators import with_curve

from eth_utils import to_hex, to_bytes
from eth_abi import encode_single, decode_single


def get_buy_price(curve_address, amount):
    return decode_single(
        "uint256",
        to_bytes(
            hexstr=eth_call(
                curve_address,
                "getBuyPrice(uint256)",
                data=encode_single("uint256", amount),
            )
        ),
    )


class BuyPrice(Resource):
    path = "/dapps/<addr>/buy-price/<int:amount>"

    @with_curve(addr="addr")
    def get(self, addr, amount, curve):
        return {
            "result": {
                "amount": str(amount),
                "price": str(get_buy_price(curve.address, amount)),
            }
        }

