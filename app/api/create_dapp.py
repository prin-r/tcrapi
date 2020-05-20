from flask_restful import Resource, abort
from app.db import db, Contract


from app.util.reqargs import with_args, Argument
from app.util.types import address

from app.util.abi_data import create_transaction


class CreateDapp(Resource):
    path = "/band/create-dapp"

    @with_args(
        Argument("name", type=str),
        Argument("symbol", type=str),
        Argument(
            "bondingCollateralEquation",
            type=list,
            location="json",
            dest="bonding_collateral_equation",
        ),
        Argument(
            "bondingLiquiditySpread", type=int, dest="bonding_liquidity_spread"
        ),
        Argument(
            "paramsExpirationTime", type=int, dest="params_expiration_time"
        ),
        Argument(
            "paramsMinParticipationPct",
            type=int,
            dest="params_min_participation_pct",
        ),
        Argument(
            "paramsSupportRequiredPct",
            type=int,
            dest="params_support_required_pct",
        ),
    )
    def post(
        self,
        name,
        symbol,
        bonding_collateral_equation,
        bonding_liquidity_spread,
        params_expiration_time,
        params_min_participation_pct,
        params_support_required_pct,
    ):
        return create_transaction(
            None,
            (
                db.session.query(Contract)
                .filter_by(contract_type="BAND_FACTORY")
                .one_or_none()
                or abort(400, message="Band factory not found")
            ).address,
            "createCommunity(string,string,uint256[],uint256,uint256,uint256,uint256)",
            ("string", name),
            ("string", symbol),
            (
                "uint256[]",
                [int(token, 0) for token in bonding_collateral_equation],
            ),
            ("uint256", bonding_liquidity_spread),
            ("uint256", params_expiration_time),
            ("uint256", params_min_participation_pct),
            ("uint256", params_support_required_pct),
        )
