#coding=utf-8

from app import repos
from . import auth

def get_user_info(username):
    return repos.get_user_by_username(username)


def create_user(data):
    existed = repos.get_user_by_username(data['username'])
    if existed:
        raise ValueError('User existed')
    new_user = repos.create_user(**data)
    return new_user


def create_session(username, password):
    user = repos.get_user_by_username(username)
    if not user or not user.verify_password(password):
        raise ValueError('username or password is wrong')
    repos.update_user(user, {'is_active': True})
    access_token = auth.generate_access_token(user.username)
    return {
        'access_token': access_token,
        'refresh_token': ''
    }


def end_session(username):
    user = repos.get_user_by_username(username)
    repos.update_user(user, {'is_active': False})
    return user
