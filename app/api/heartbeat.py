from flask_restful import Resource


class Heartbeat(Resource):
    path = "/heartbeat"

    def get(self):
        return {}
