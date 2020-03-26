#coding=utf-8
"""Security module
"""

from datetime import datetime
import six
from werkzeug.exceptions import Unauthorized
from connexion import context
from jose import jwt
from app import config
from app import models


def decode_token(access_token):
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
        user = models.session.query(models.User).filter(        # pylint: disable=E1101
            models.User.username == payload.get('data')['username']
        ).first()
        if not user:
            raise Unauthorized()
        context['current_user'] = user
    except jwt.JWTError as decode_error:
        six.raise_from(Unauthorized, decode_error)
    else:
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
