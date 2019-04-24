from core.admin import BaseAdminModelView, ImmutableAdminView
from core.models import db

from mlm.models import MlmAccount


def init(admin):
    admin.add_view(ImmutableAdminView(MlmAccount, db.session, category='Mlm'))
