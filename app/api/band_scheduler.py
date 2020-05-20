from flask_restful import Resource

from app.util.reqargs import with_args, Argument
from app.util.types import address
from app.util.eth_sendTransaction import send_scheduler


class BandScheduler(Resource):
    path = "/band/scheduler"

    @with_args(
        Argument("to", type=address),
        Argument("data", type=str),
        Argument("when", type=str),
    )
    def post(self, to, data, when):
        send_scheduler(to, data, when)
        return {"status": "OK"}
