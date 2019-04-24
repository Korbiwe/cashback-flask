from flask_security.utils import verify_and_update_password
from auth.models import User


def authenticate(credential, password):
    user = User.get_by_credential(credential)
    if user and verify_and_update_password(password, user):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()
