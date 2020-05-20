import os

from datetime import datetime
from decimal import Decimal

from flask import Flask
from flask.json import JSONEncoder
from flask_cors import CORS
from flask_graphql import GraphQLView
from flask_sslify import SSLify
from flask_restful import Api
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from app.api import setup_routes


app = Flask(__name__)
CORS(app)
SSLify(app)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat() + "Z"
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            super.default(obj)


app.config["SECRET_KEY"] = os.getenv("BANDWEB_SECRET", "eOxXTOF6v6")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_ECHO"] = os.getenv("SQLALCHEMY_ECHO", True)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
if not os.getenv("DATABASE_URI").startswith("sqlite"):
    app.config["SQLALCHEMY_POOL_SIZE"] = 3
app.config["RESTFUL_JSON"] = {"cls": CustomJSONEncoder}


api = Api(app)
db = SQLAlchemy(app)
socketio = SocketIO(app)
setup_routes(api)

# from app.graphql import schema

# app.add_url_rule(
#     "/graphql",
#     view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
# )
# # Optional, for adding batch query support (used in Apollo-Client)
# app.add_url_rule(
#     "/graphql/batch",
#     view_func=GraphQLView.as_view("graphql", schema=schema, batch=True),
# )

