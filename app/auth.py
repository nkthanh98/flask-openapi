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
        time_delta = datetime.now().timestamp() - payload.get('timestamp', 0)
        if time_delta > config.LOGIN_TIME_ALIVE:
            raise Unauthorized('Login time to expired')
        user = repos.get_user_by_username(payload['data']['username'])
        if not user or not user.is_active:
            raise Unauthorized()
    except jwt.JWTError as decode_error:
        six.raise_from(Unauthorized, decode_error)
    else:
        if callback:
            callback(user)
        return payload


def generate_access_token(data):        # pylint: disable=C0116
    payload = {
        'data': data,
        'timestamp': datetime.now().timestamp()
    }
    return jwt.encode(
        claims=payload,
        key=config.JWT_KEY,
        algorithm=config.JWT_ALGORITHM
    )


auth_fn = partial(decode_token, callback=set_current_user)
