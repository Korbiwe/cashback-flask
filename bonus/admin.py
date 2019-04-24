from core.admin import ImmutableAdminView
from core.models import db

from bonus.models import (
    PaymentTransaction, PaymentRequest, PartnerWithdrawTransaction, MlmWithdrawTransaction,
    ClientDepositTransaction, MlmBonusTransaction, ClientBonusTransaction
)


def init(admin):
    admin.add_view(ImmutableAdminView(PaymentRequest, db.session, category='Bonus'))
    admin.add_view(ImmutableAdminView(PaymentTransaction, db.session, category='Bonus'))
    admin.add_view(ImmutableAdminView(PartnerWithdrawTransaction, db.session, category='Bonus'))
    admin.add_view(ImmutableAdminView(MlmBonusTransaction, db.session, category='Bonus'))
    admin.add_view(ImmutableAdminView(ClientDepositTransaction, db.session, category='Bonus'))
    admin.add_view(ImmutableAdminView(MlmWithdrawTransaction, db.session, category='Bonus'))
    admin.add_view(ImmutableAdminView(ClientBonusTransaction, db.session, category='Bonus'))
