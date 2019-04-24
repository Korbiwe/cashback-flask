from flask import Blueprint

partners = Blueprint('partners', __name__, url_prefix='/api/v1/partners')

from . import views, models
