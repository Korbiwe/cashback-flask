import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECURITY_POST_LOGIN_VIEW = '/admin'
    SECURITY_USER_IDENTITY_ATTRIBUTES = 'email'
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'whysosalty'

    JWT_AUTH_USERNAME_KEY = 'credential'
    JWT_AUTH_URL_RULE = '/api/v1/auth/jwt'
    # TODO: This is for debug only
    JWT_VERIFY_EXPIRATION = False
    JWT_EXPIRATION_DELTA = timedelta(days=7)

    SECRET_KEY = 'wow change me daddy' or os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite') or \
                              os.environ.get('DATABASE_URL')

    DEBUG = os.environ.get('FLASK_DEBUG', True)

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    BONUS_PAYMENT_REQUEST_EXPIRATION = timedelta(days=1)

    ENABLED_MODULES = [
        'core',
        'auth',
        'partners',
        'clients',
        'mlm',
        'bonus'
    ]
