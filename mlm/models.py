from core.models import db, BaseModel


class MlmAccount(BaseModel):
    __tablename__ = 'mlm_account'

    user = db.relationship("User", uselist=False, backref="mlm_account")

    def __str__(self):
        return f'<MlmAccount id={self.id} user={self.user.phone}>'
