import os

from uuid import uuid4

from flask import jsonify


def json_response(result: dict, **kwargs):
    if result is not None:
        return jsonify(success=True, error=None, result=result, **kwargs)
    elif len(kwargs) != 0:
        return jsonify(success=True, error=None, result=kwargs)
    else:
        return jsonify(success=True, error=None, result=None)


def random_uuid4_as_hex():
    return uuid4().hex
