from sqlalchemy import or_

from flask_security import UserMixin, RoleMixin

from core.models import db, BaseModel

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    login = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('role', lazy='dynamic'))

    partner_account_id = db.Column(db.Integer, db.ForeignKey('partner_account.id'))
    mlm_account_id = db.Column(db.Integer, db.ForeignKey('mlm_account.id'))
    client_account_id = db.Column(db.Integer, db.ForeignKey('client_account.id'))
    # TODO: reverse the relationship

    def __str__(self):
        return f'User<id={self.id}>'

    @staticmethod
    def get_by_credential(credential):
        return User.query.filter(or_(User.email == credential, User.phone == credential, User.login == credential)).first()

    def as_dict(self):
        result = super(User, self).as_dict()
        result['password'] = '<redacted>'
        return result


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    # Our Role has three fields, ID, name and description
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)
