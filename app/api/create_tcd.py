from flask_restful import Resource, abort
from app.db import db, Contract
from eth_utils import to_checksum_address

from app.util.reqargs import with_args, Argument
from app.util.types import address

from app.util.abi_data import create_transaction


class CreateTCD(Resource):
    path = "/dapps/<addr>/create-tcd"

    @with_args(
        Argument("minProviderStake", type=int, dest="min_provider_stake"),
        Argument("maxProviderCount", type=int, dest="max_provider_count"),
        Argument("ownerRevenuePct", type=int, dest="owner_revenue_pct"),
        Argument("queryPrice", type=int, dest="query_price"),
    )
    def post(
        self,
        addr,
        min_provider_stake,
        max_provider_count,
        owner_revenue_pct,
        query_price,
    ):
        return create_transaction(
            None,
            addr,
            "createTCD(uint256,uint256,uint256,uint256)",
            ("uint256", min_provider_stake),
            ("uint256", max_provider_count),
            ("uint256", owner_revenue_pct),
            ("uint256", query_price),
        )
