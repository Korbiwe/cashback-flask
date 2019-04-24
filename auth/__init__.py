from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

from . import models, views
