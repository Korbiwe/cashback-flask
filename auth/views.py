from flask_jwt import jwt_required, current_identity

from core.utils import json_response

from auth import auth


@auth.route('/me')
@jwt_required()
def me():
    client = current_identity.client_account
    partner = current_identity.partner_account
    return json_response({
        **current_identity.as_dict(),
        'client': client.as_dict() if client else None,
        'partner': partner.as_dict() if partner else None,
    })
