from traceback import format_exc

from flask import jsonify

from werkzeug.exceptions import HTTPException

from config import Config

from . import core


@core.app_errorhandler(HTTPException)
def handle_http_errors(e: HTTPException):
    if 300 <= e.code <= 399:
        return e
    if 400 <= e.code <= 499:
        return jsonify(success=False, error=str(e), traceback=format_exc(), result=None), e.code
    if 500 <= e.code <= 599:
        if Config.DEBUG:
            return jsonify(success=False, error=str(e), traceback=format_exc(), result=None), e.code
        else:
            return jsonify(success=False, error='Internal server error.', result=None), e.code


@core.app_errorhandler(Exception)
def handle_all_uncaught_errors(e: Exception):
    if Config.DEBUG:
        return jsonify(success=False, error=str(e), traceback=format_exc(), result=None), 500
    else:
        return jsonify(success=False, error='Something went really wrong. Please report this.', result=None), 500
