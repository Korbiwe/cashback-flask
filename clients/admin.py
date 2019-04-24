from core.admin import BaseAdminModelView
from core.models import db

from clients.models import ClientAccount


def init(admin):
    admin.add_view(BaseAdminModelView(ClientAccount, db.session, category='Client'))
