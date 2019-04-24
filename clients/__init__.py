from flask import Blueprint

clients = Blueprint('clients', __name__, url_prefix='/api/v1/clients')

from . import views, models
