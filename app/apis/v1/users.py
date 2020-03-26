# coding=utf-8

from connexion import request
from werkzeug.exceptions import BadRequest
from app.models import (
    User,
    session,
)
from app import auth


def get_user(user_id):
    return session.query(User).filter(
        User.id == user_id
    ).one_or_none()


def create_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        fullname=data['fullname']
    )
    new_user.password = data['password']
    session.add(new_user)
    session.commit()
    return new_user.dump()


def login():
    data = request.get_json()
    user = session.query(User).filter(
        User.username == data['username']
    ).one_or_none()
    if not user:
        raise BadRequest('username or password is wrong')
    if not user.verify_password(data['password']):
        raise BadRequest('username or password is wrong')
    access_token = auth.generate_access_token({
        'username': user.username
    })
    return {
        'access_token': access_token,
        'refresh_token': ''
    }
