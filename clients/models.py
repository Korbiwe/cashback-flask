from core.models import db, BaseModel


class ClientAccount(BaseModel):
    __tablename__ = 'client_account'
    fullname = db.Column(db.String(255), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    user = db.relationship("User", uselist=False, backref="client_account")

    def __str__(self):
        return f'<ClientAccount id={self.id} fullname={self.fullname} user={self.user.phone}>'

    def as_dict(self):
        res = super(ClientAccount, self).as_dict()
        res['balance'] = self.balance
        return res

    @property
    def balance(self):
        balance = 0
        payment_transactions = self.payment_transactions
        deposit_transactions = self.deposit_transactions

        for t in payment_transactions:
            balance -= t.amount

        for t in deposit_transactions:
            balance += t.amount

        return balance
