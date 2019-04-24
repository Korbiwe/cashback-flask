from flask import Blueprint

mlm = Blueprint('mlm', __name__, url_prefix='/api/v1/mlm')

from . import models, lib
