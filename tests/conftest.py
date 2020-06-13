# coding=utf-8

import pytest
from app import (
    models,
    http,
)


@pytest.fixture
def db():
    models.Base.metadata.create_all(bind=models.session.get_bind())
    yield models.session


@pytest.fixture
@pytest.mark.usefixtures('db')
def client(request, db):
    _wsgi = http.create_wsgi()
    with _wsgi.app.test_client() as _client:
        if request.cls is not None:
            request.cls.client = _client
        yield _client
