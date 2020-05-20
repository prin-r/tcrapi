from flask_restful import abort
from functools import wraps

from app.db import db, Contract, Community, Curve, Parameter, TCR


def with_community(addr="addr", name="comm"):
    def decorator_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if addr in kwargs:
                core_addr = kwargs[addr]
                community = (
                    db.session.query(Community).get(core_addr)
                ) or abort(400, message=f"Unknown dApp with {core_addr}")
                kwargs[name] = community
            return f(*args, **kwargs)

        return wrapper

    return decorator_function


def with_curve(addr="addr", name="curve"):
    def decorator_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if addr in kwargs:
                core_addr = kwargs[addr]
                curve = db.session.query(Curve).filter_by(
                    community_address=core_addr
                ).one_or_none() or abort(
                    400, message=f"Not found curve on this core address"
                )
                kwargs[name] = curve
            return f(*args, **kwargs)

        return wrapper

    return decorator_function


def with_parameter(addr="addr", name="param"):
    def decorator_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if addr in kwargs:
                core_addr = kwargs[addr]
                parameter = db.session.query(Parameter).filter_by(
                    community_address=core_addr
                ).one_or_none() or abort(
                    400, message=f"Not found parameter on this core address"
                )
                kwargs[name] = parameter
            return f(*args, **kwargs)

        return wrapper

    return decorator_function


def with_poll_contract(addr="addr", name="poll_contract"):
    def decorator_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if addr in kwargs:
                contract = (
                    db.session.query(Contract)
                    .filter_by(address=kwargs[addr])
                    .one_or_none()
                )
                if contract.contract_type == "CORE":
                    parameter_contract = db.session.query(Parameter).filter_by(
                        community_address=kwargs[addr]
                    ).one_or_none() or abort(
                        400,
                        message=f"Unknow parameter contract for dApp with ID {contract.address}",
                    )
                    kwargs[name] = parameter_contract
                elif contract.contract_type == "TCR":
                    kwargs[name] = db.session.query(TCR).get(
                        kwargs[addr]
                    ) or abort(400, message=f"TCR not found")
                else:
                    abort(
                        400,
                        message=f"Wrong contract type for {contract.address}",
                    )
                return f(*args, **kwargs)

        return wrapper

    return decorator_function


def with_tcr(addr="addr", name="tcr_contract"):
    def decorator_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if addr in kwargs:
                kwargs[name] = db.session.query(TCR).get(kwargs[addr]) or abort(
                    400, message=f"TCr not found"
                )
            return f(*args, **kwargs)

        return wrapper

    return decorator_function
