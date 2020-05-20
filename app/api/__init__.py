def setup_routes(api):

    from app.api.heartbeat import Heartbeat
    from app.api.buy_price import BuyPrice
    from app.api.sell_price import SellPrice
    from app.api.band_transfer import BandTransfer
    from app.api.token_transfer import TokenTransfer
    from app.api.buy_token import BuyToken
    from app.api.sell_token import SellToken

    from app.api.create_dapp import CreateDapp
    from app.api.create_tcr import CreateTCR
    from app.api.create_tcd import CreateTCD
    from app.api.parameter.propose import ProposeProposal

    from app.api.band_request import BandRequest
    from app.api.token_request import TokenRequest

    from app.api.band_feeless import BandFeeless
    from app.api.band_exec import BandExec
    from app.api.band_scheduler import BandScheduler

    # TCR entry
    from app.api.tcr.entries import TCREntries
    from app.api.tcr.deposit import TCRDeposit
    from app.api.tcr.withdraw import TCRWithdraw
    from app.api.tcr.exit import TCRExit
    from app.api.tcr.challenge import TCRChallenge
    from app.api.tcr.reward import TCRClaimReward
    from app.api.tcr.min_deposit import TCRMinDeposit

    # Voting
    from app.api.voting.castvote import CastVote
    from app.api.voting.commitvote import CommitVote
    from app.api.voting.revealvote import RevealVote
    from app.api.voting.voting_power import VotingPower

    # Data
    from app.api.tcd.register_source import RegisterSource
    from app.api.tcd.vote_source import VoteSource
    from app.api.tcd.exit_source import KickSource
    from app.api.tcd.withdraw_source import WithdrawSource
    from app.api.tcd.distribute_fee import DistributeFee
    from app.api.tcd.get_data import GetDataAsNumber

    RESOURCES = [
        Heartbeat,
        BuyPrice,
        SellPrice,
        BandTransfer,
        TokenTransfer,
        BuyToken,
        SellToken,
        CreateDapp,
        CreateTCR,
        CreateTCD,
        ProposeProposal,
        BandRequest,
        TokenRequest,
        BandFeeless,
        BandExec,
        BandScheduler,
        TCREntries,
        TCRDeposit,
        TCRWithdraw,
        TCRExit,
        TCRChallenge,
        TCRClaimReward,
        TCRMinDeposit,
        CastVote,
        CommitVote,
        RevealVote,
        VotingPower,
        RegisterSource,
        VoteSource,
        KickSource,
        WithdrawSource,
        DistributeFee,
        GetDataAsNumber,
    ]

    for resource in RESOURCES:
        api.add_resource(resource, resource.path)
