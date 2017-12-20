from flask import request, Response
from functools import wraps
from jsonschema import FormatChecker, validate, ValidationError


"""
Validates JSON for endpoints
"""


def validate_payload(schema=None):

    def json_decorator(func):
        @wraps(func)
        def json_validator(*args, **kwargs):
            payload = request.get_json(force=True)
            if not payload:
                return Response(status=400)
            if schema:
                try:
                    validate(payload, schema, format_checker=FormatChecker())
                except ValidationError as e:  # NOQA
                    return Response(status=400)

            return func(*args, **kwargs)

        return json_validator

    return json_decorator
