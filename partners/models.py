from core.models import db, BaseModel


def default_display_name(context):
    return context.get_current_parameters()['official_name']


class PartnerAccount(BaseModel):
    __tablename__ = 'partner_account'

    individual_taxpayer_number = db.Column(db.String(12), unique=True, nullable=False)
    display_name = db.Column(db.String(255), default=default_display_name)
    official_name = db.Column(db.String(255), nullable=False)
    verified = db.Column(db.Boolean, default=False)

    user = db.relationship("User", uselist=False, backref='partner_account')

    def __str__(self):
        return f'<PartnerAccount id={self.id} display_name={self.display_name} user={self.user.phone}>'

    def as_dict(self):
        res = super(PartnerAccount, self).as_dict()
        res['balance'] = self.balance
        return res

    @property
    def balance(self):
        balance = 0
        payment_transactions = self.payment_transactions
        withdraw_transactions = self.withdraw_transactions

        for t in payment_transactions:
            balance += t.amount

        for t in withdraw_transactions:
            if t.confirmed and not t.rejected:
                balance -= t.amount

        return balance
