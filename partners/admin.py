from core.admin import BaseAdminModelView
from core.models import db

from partners.models import (
    PartnerAccount
)


def init(admin):
    admin.add_view(BaseAdminModelView(PartnerAccount, db.session, category='Partners'))
