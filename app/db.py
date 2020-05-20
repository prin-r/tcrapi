import decamelize
import inflect

from sqlalchemy import Table, inspect, func
from sqlalchemy.ext.automap import (
    automap_base,
    generate_relationship,
    interfaces,
)
from sqlalchemy.event import listens_for
from sqlalchemy.orm.query import Query

from app.core import db

from decimal import Decimal

_pluralizer = inflect.engine()


def _gen_relationship(
    base, direction, return_fn, attrname, local_cls, referred_cls, **kw
):
    return generate_relationship(
        base, direction, return_fn, attrname, local_cls, referred_cls, **kw
    )


@listens_for(Table, "column_reflect")
def column_reflect(inspector, table, column_info):
    column_info["key"] = decamelize.convert(column_info["name"])


Base = automap_base()
Base.prepare(db.engine, reflect=True, generate_relationship=_gen_relationship)


Community = Base.classes.community
Token = Base.classes.token
Curve = Base.classes.curve
Challenge = Base.classes.challenge
Contract = Base.classes.contract
Parameter = Base.classes.parameter
Proposal = Base.classes.proposal
Challenge = Base.classes.challenge
TCR = Base.classes.tcr
DelegatedTransaction = Base.classes.delegated_tx
Entry = Base.classes.entry
EntryHistory = Base.classes.entry_history
Transfer = Base.classes.transfer

