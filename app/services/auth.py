#coding=utf-8
"""Security module
"""

from datetime import datetime
from functools import partial
from werkzeug.exceptions import Unauthorized
from connexion import context
from jose import jwt
from app import repos

from . import _config


def set_current_user(user):
    context['current_user'] = user


def decode_token(access_token, callback=None):
    """Decode JWT token for secure api

    :param access_token:
    """
    try:
        payload = jwt.decode(
            token=access_token,
            key=_config.JWT_KEY,
            algorithms=_config.JWT_ALGORITHM
        )
        user = repos.get_user_by_username(payload['sub'])
        if not user or not user.is_active:
            raise Unauthorized()
    except jwt.JWTError as decode_error:
        raise Unauthorized from decode_error
    else:
        if callback:
            callback(user)
        return payload


def _get_timestamp():
    return datetime.now().timestamp()


def generate_access_token(identifier):        # pylint: disable=C0116
    timestamp = _get_timestamp()
    payload = {
        'sub': identifier,
        'iss': _config.ISSUE_MAINTAINER,
        'iat': int(timestamp),
        'exp': int(timestamp + _config.LOGIN_TIME_ALIVE)
    }
    return jwt.encode(
        claims=payload,
        key=_config.JWT_KEY,
        algorithm=_config.JWT_ALGORITHM
    )


auth_fn = partial(decode_token, callback=set_current_user)
