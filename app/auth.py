#coding=utf-8
"""Security module
"""

from datetime import datetime
from functools import partial
import six
from werkzeug.exceptions import Unauthorized
from connexion import context
from jose import jwt
from app import config
from app import repos


def set_current_user(user):
    context['current_user'] = user


def decode_token(access_token, callback=None):
    """Decode JWT token for secure api

    :param access_token:
    """
    try:
        payload = jwt.decode(
            token=access_token,
            key=config.JWT_KEY,
            algorithms=config.JWT_ALGORITHM
        )
        user = repos.get_user_by_username(payload['sub'])
        if not user or not user.is_active:
            raise Unauthorized()
    except jwt.JWTError as decode_error:
        six.raise_from(Unauthorized, decode_error)
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
        'iss': config.ISSUE_MAINTAINER,
        'iat': int(timestamp),
        'exp': int(timestamp + config.LOGIN_TIME_ALIVE)
    }
    return jwt.encode(
        claims=payload,
        key=config.JWT_KEY,
        algorithm=config.JWT_ALGORITHM
    )


auth_fn = partial(decode_token, callback=set_current_user)
