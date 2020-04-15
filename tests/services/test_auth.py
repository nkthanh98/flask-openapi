# coding=utf-8

from tests import faker
from app import models
from app.services import auth


def test_encode_and_decode_token(db):
    user = models.User(
        fullname=faker.name(),
        username=faker.name(),
        password=faker.text(16)
    )
    user.is_active = True
    db.add(user)
    db.commit()
    access_token = auth.generate_access_token(user.username)

    data_decoded = auth.decode_token(access_token)
    assert data_decoded['sub'] == user.username
