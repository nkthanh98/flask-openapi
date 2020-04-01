# coding=utf-8

from connexion import (
    request,
    context,
    NoContent
)
from werkzeug.exceptions import BadRequest
from app import auth
from app import utils
from app import repos
from . import user_schema


def get_user_info(user):
    user = repos.get_user_by_username(user)
    return utils.dump(user_schema.User, user)


def create_user():
    data = request.get_json()
    new_user = repos.create_user(**data)
    return {
        'id': new_user.id
    }, 201


def login():
    data = request.get_json()
    user = repos.get_user_by_username(data['username'])
    if not user:
        raise BadRequest('username or password is wrong')
    if not user.verify_password(data['password']):
        raise BadRequest('username or password is wrong')
    repos.update_user(user, {'is_active': True})
    access_token = auth.generate_access_token({
        'username': user.username
    })
    return {
        'access_token': access_token,
        'refresh_token': ''
    }


def logout(user):
    user = repos.get_user_by_username(user)
    repos.update_user(user, {'is_active': False})
    return NoContent
