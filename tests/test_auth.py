# coding=utf-8

from tests import faker
from app import (
    auth,
    models,
)


def test_encode_and_decode_token(client):
    user = models.User(
        fullname=faker.name(),
        username=faker.name(),
        password=faker.text(16)
    )
    user.is_active = True
    models.session.add(user)
    models.session.commit()
    access_token = auth.generate_access_token(user.username)

    data_decoded = auth.decode_token(access_token)
    assert data_decoded['sub'] == user.username
