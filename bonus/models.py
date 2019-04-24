import random
import string
from datetime import datetime

from config import Config
from core.models import db, BaseModel

from partners.models import PartnerAccount
from clients.models import ClientAccount
from mlm.models import MlmAccount


def get_random_code():
    return ''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(8)])


class PaymentRequest(BaseModel):
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    code = db.Column(
        db.String(8),
        default=get_random_code
    )

    from_ = db.relationship('ClientAccount', backref='payment_requests')
    from_id = db.Column(db.Integer, db.ForeignKey('client_account.id'), nullable=False)
    to_ = db.relationship('PartnerAccount', backref='payment_requests')
    to_id = db.Column(db.Integer, db.ForeignKey('partner_account.id'), nullable=False)

    def confirm(self, code):
        if datetime.now() > self.created_at + Config.BONUS_PAYMENT_REQUEST_EXPIRATION:
            self.soft_delete()
            raise ValueError('Payment request expired!')
        if code != self.code:
            raise ValueError('Invalid code!')

        new_payment_transaction = PaymentTransaction(
            amount=self.amount,
            description=self.description,
            to_=self.to_,
            from_=self.from_
        )

        db.session.add(new_payment_transaction)
        self.soft_delete()
        db.session.commit()

        return new_payment_transaction


class PartnerWithdrawTransaction(BaseModel):
    amount = db.Column(db.Float, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    rejected = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(255))

    partner_account_id = db.Column(db.Integer, db.ForeignKey('partner_account.id'), nullable=False)
    partner_account = db.relationship('PartnerAccount', backref='withdraw_transactions')


class ClientDepositTransaction(BaseModel):
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))

    client_account_id = db.Column(db.Integer, db.ForeignKey('client_account.id'), nullable=False)
    client_account = db.relationship('ClientAccount', backref='deposit_transactions')


class MlmWithdrawTransaction(BaseModel):
    amount = db.Column(db.Float, nullable=False)
    rejected = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(255))

    mlm_account_id = db.Column(db.Integer, db.ForeignKey('mlm_account.id'), nullable=False)
    mlm_account = db.relationship('MlmAccount', backref='withdraw_transactions')


class MlmBonusTransaction(BaseModel):
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))

    mlm_account_id = db.Column(db.Integer, db.ForeignKey('mlm_account.id'), nullable=False)
    mlm_account = db.relationship('MlmAccount', backref='bonus_transactions')


class ClientBonusTransaction(BaseModel):
    amount = db.Column(db.Float, nullable=False)

    client_account_id = db.Column(db.Integer, db.ForeignKey('client_account.id'), nullable=False)
    client_account = db.relationship('ClientAccount', backref='bonus_transaction')


class PaymentTransaction(BaseModel):
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))

    from_ = db.relationship('ClientAccount', backref='payment_transactions')
    from_id = db.Column(db.Integer, db.ForeignKey('client_account.id'), nullable=False)
    to_ = db.relationship('PartnerAccount', backref='payment_transactions')
    to_id = db.Column(db.Integer, db.ForeignKey('partner_account.id'), nullable=False)
