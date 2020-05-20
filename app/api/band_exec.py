from flask_restful import Resource

from app.util.reqargs import with_args, Argument
from app.util.types import address
from app.util.eth_sendTransaction import eth_sendTransaction


class BandExec(Resource):
    path = "/band/exec"

    @with_args(Argument("to", type=address), Argument("data", type=str))
    def post(self, to, data):
        return {"result": eth_sendTransaction(to, data)}
