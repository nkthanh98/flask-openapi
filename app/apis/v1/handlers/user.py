# coding=utf-8

import six
from connexion import (
    request,
    NoContent
)
from werkzeug.exceptions import BadRequest
from app import (
    utils,
    services,
)
from ..schemas import user as user_schema


def get_user_info(user):
    user = services.get_user_info(user)
    return utils.dump(user_schema.User, user)


def create_user():
    try:
        data = request.get_json()
        new_user = services.create_user(data)
    except ValueError as error:
        raise BadRequest(str(error)) from error
    else:
        return {
            'id': new_user.id
        }, 201


def login():
    try:
        data = request.get_json()
        session_info = services.create_session(data['username'], data['password'])
    except ValueError as error:
        raise BadRequest(str(error)) from error
    else:
        return session_info


def logout(user):
    try:
        services.end_session(user)
    except ValueError as error:
        raise BadRequest(str(error)) from error
    else:
        return NoContent
