# coding=utf-8

import pytest
from app import (
    apis,
    models
)


@pytest.fixture
def client(request):
    _wsgi = apis.create_wsgi()
    models.init(
        drive='sqlite',
        credentials={
            'database': ':memory:'
        }
    )
    models.Base.metadata.create_all(bind=models.session.get_bind())
    with _wsgi.app.test_client() as _client:
        if request.cls is not None:
            request.cls.client = _client
        yield _client
