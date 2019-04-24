#!/usr/bin/env python
import importlib

from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security
from flask_admin import Admin
from flask_jwt import JWT
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from core.models import db
from auth.models import User, Role
from auth.helpers import init_security
from auth.jwt import authenticate, identity

from config import Config

sentry_sdk.init(
    dsn="https://d69c8f5599ae401390ec09661b38bad3@sentry.io/1446049",
    integrations=[FlaskIntegration()],
    send_default_pii=True
)

security = Security()
app = Flask(__name__)

app.config.from_object(Config)

admin = Admin(base_template='admin/master.html', template_mode='bootstrap3')

db.init_app(app)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security_ctx = security.init_app(
    app, user_datastore
)
admin.init_app(app)
jwt = JWT(app, authenticate, identity)

# init flask-admin views
# from auth.admin import init as init_auth_admin_models
# init_auth_admin_models(admin)
# from partners.admin import init as init_partners_models
# init_partners_models(admin)
# from clients.admin import init as init_clients_models
# init_clients_models(admin)
# from mlm.admin import init as init_mlm_models
# init_mlm_models(admin)
# from bonus.admin import init as init_bonus_models
# init_bonus_models(admin)

for module_name in Config.ENABLED_MODULES:
    module = importlib.import_module(module_name)
    # blueprint names are the same as the names. i.e. the blueprint in core will be located at core.core
    blueprint = getattr(module, module_name)
    admin_module = importlib.import_module(f'{module_name}.admin')
    app.register_blueprint(blueprint)
    admin_module.init(admin)


@app.before_first_request
def before_first_request():
    init_security(user_datastore)

