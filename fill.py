from app.db import *

for challenge in (
    db.session.query(EntryEvent).filter_by(action="CHALLENGED").all()
):
    challenger = (
        db.session.query(Challenge.challenger)
        .filter_by(block_id=challenge.block_id, log_index=challenge.log_index)
        .first()
    )[0]
    challenge.actor = challenger
    # print(challenge.id, challenger)

db.session.commit()
