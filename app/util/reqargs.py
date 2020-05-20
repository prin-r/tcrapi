from flask_restful import reqparse
from functools import wraps


class Argument(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        if "required" not in kwargs:
            kwargs["required"] = True


def with_args(*arguments):
    parser = reqparse.RequestParser()

    for argument in arguments:
        if isinstance(argument, Argument):
            parser.add_argument(*argument.args, **argument.kwargs)

    def decorator_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if len(parser.args) != 0:
                return f(*args, **kwargs, **parser.parse_args(strict=True))
            else:
                return f(*args, **kwargs)

        return wrapper

    return decorator_function
