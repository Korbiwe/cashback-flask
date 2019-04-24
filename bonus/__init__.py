from flask import Blueprint

bonus = Blueprint('bonus', __name__, url_prefix='/api/v1/bonus')

from . import models, views
