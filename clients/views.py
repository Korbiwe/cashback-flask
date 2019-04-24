from flask import (
    abort, request
)

from jsonschema import validate, ValidationError

from flask_jwt import current_identity, jwt_required

from core.models import db
from core.utils import json_response
from auth.models import User
from clients import clients
from clients.models import ClientAccount
from clients.schemas import create_schema, bind_schema
from bonus.models import ClientDepositTransaction, ClientBonusTransaction


# noinspection PyArgumentList
@clients.route('/create_new', methods=['POST'])
def create_new():
    data = request.get_json()
    try:
        validate(data, create_schema)
    except ValidationError as e:
        return abort(400, str(e))

    existing_user = User.get_by_credential(data['login']) or \
                    User.get_by_credential(data['phone']) or \
                    User.get_by_credential(data['email'])
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

    if user.client_account_id:
        return abort(400, 'You already have a client account!')

    new_client_account = ClientAccount(
        fullname=data['fullname']
    )

    new_client_account.user = user

    db.session.add(new_client_account)
    db.session.add(user)
    db.session.commit()

    return json_response(user.as_dict()), 201


@clients.route('/bind', methods=['POST'])
@jwt_required()
def bind_to_existing():
    data = request.get_json()
    try:
        validate(data, bind_schema)
    except ValidationError as e:
        return abort(400, str(e))

    if current_identity.partner_account_id:
        return abort(400, 'You already have a partner account!')

    try:
        new_client_account = ClientAccount(
            fullname=data['fullname']
        )
    except KeyError as e:
        return abort(400, f'Field {str(e)} is missing!')

    new_client_account.user = current_identity

    db.session.add(new_client_account)

    db.session.commit()

    return json_response(new_client_account.as_dict()), 201


@clients.route('/deposit', methods=['POST'])
@jwt_required()
def deposit():
    data = request.get_json()

    client_account = ClientAccount.query.filter_by(id=current_identity.client_account_id).first()

    if not client_account:
        return abort(403, 'You don\'t have a client account!')

    new_transaction = ClientDepositTransaction(
        amount=data['amount'],
        description=data['description'],
        client_account=client_account
    )

    new_bonus = ClientBonusTransaction(
        amount=data['amount'] * 0.03,
        client_account=client_account
    )

    db.session.add(new_transaction)
    db.session.add(new_bonus)
    db.session.commit()

    return json_response({
        'deposited': new_transaction.as_dict(),
        'bonus': new_bonus.as_dict()
    }), 201


@clients.route('/me')
@jwt_required()
def me():
    account = current_identity.client_account

    if not account:
        return abort(404, 'You have no client account!')

    return json_response(account.as_dict())


