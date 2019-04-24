from flask import (
    abort, request
)

from jsonschema import validate, ValidationError

from flask_jwt import current_identity, jwt_required

from core.models import db
from core.utils import json_response
from auth.models import User
from partners import partners
from partners.models import PartnerAccount
from clients.models import ClientAccount
from bonus.models import PaymentRequest
from notifications import send_sms

from partners.schemas import (
    confirm_payment_schema, create_schema, request_payment_schema, bind_schema
)


# noinspection PyArgumentList
@partners.route('/create_new', methods=['POST'])
def create_new():
    data = request.get_json()
    try:
        validate(data, create_schema)
    except ValidationError as e:
        return abort(400, str(e))
    existing_user = User.get_by_credential(data['login']) \
        or User.get_by_credential(data['phone']) \
        or User.get_by_credential(data['email'])
    if existing_user:
        user = existing_user
    else:
        user = User(
            login=data['login'],
            email=data['email'],
            phone=data['phone'],
            password=data['password'],
            active=True
        )

    if user.partner_account_id:
        return abort(400, 'You already have a partner account!')

    new_partner_account = PartnerAccount(
        individual_taxpayer_number=data['individual_taxpayer_number'],
        display_name=data['display_name'],
        official_name=data['official_name'],
    )

    new_partner_account.user = user

    db.session.add(new_partner_account)
    db.session.add(user)
    db.session.commit()

    return json_response(user.as_dict()), 201


@partners.route('/bind', methods=['POST'])
@jwt_required()
def bind_to_existing():
    data = request.get_json()
    try:
        validate(data, bind_schema)
    except ValidationError as e:
        return abort(400, str(e))

    if current_identity.partner_account_id:
        return abort(400, 'You already have a partner account!')

    new_partner_account = PartnerAccount(
        individual_taxpayer_number=data['individual_taxpayer_number'],
        display_name=data['display_name'],
        official_name=data['official_name'],
    )

    new_partner_account.user = current_identity

    db.session.add(new_partner_account)

    db.session.commit()

    return json_response(new_partner_account.as_dict()), 201


@partners.route('/request_payment', methods=['POST'])
@jwt_required()
def request_payment():
    data = request.get_json()
    try:
        validate(data, request_payment_schema)
    except ValidationError as e:
        return abort(400, str(e))

    if not current_identity.partner_account_id:
        return abort(403, 'You are not a partner!')

    partner_account = PartnerAccount.query.filter_by(id=current_identity.partner_account_id).first()
    client_user = User.get_by_credential(data['credential'])

    if not client_user:
        return abort(400, 'No such user!')

    if not client_user.client_account_id:
        return abort(400, 'This user is not a client!')

    client_account = ClientAccount.query.filter_by(
       id=client_user.client_account_id
    ).first()

    if client_account.balance < data['amount']:
        return abort(400, 'Client doesn\'t have enough money!')

    if current_identity.id == client_account.id:
        return abort(400, 'You can\'t request payment from your own client account!')

    new_request = PaymentRequest(
        amount=data['amount'],
        description=data['description'],
        to_=partner_account,
        from_=client_account
    )

    db.session.add(new_request)
    db.session.commit()

    send_sms([client_user.phone], text=new_request.code)

    response = new_request.as_dict()
    response['code'] = '<redacted>'
    return json_response(response)


@partners.route('/confirm_payment', methods=['POST'])
@jwt_required()
def confirm_payment():
    data = request.get_json()

    try:
        validate(data, confirm_payment_schema)
    except ValidationError as e:
        return abort(400, str(e))

    if not current_identity.partner_account_id:
        return abort(403, 'You are not a partner!')

    payment_request = PaymentRequest.query.filter_by(id=data['request_id']).first()

    if not payment_request:
        abort(400, 'No such payment request!')

    if payment_request.to_id != current_identity.partner_account_id:
        return abort(403, 'That is not your payment!')

    transaction = payment_request.confirm(data['code'])

    return json_response(transaction.as_dict())


@partners.route('/me')
@jwt_required()
def me():
    account = current_identity.partner_account

    if not account:
        return abort(404, 'You have no partner account.')

    return json_response(account.as_dict())

