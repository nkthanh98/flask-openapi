# coding=utf-8

import pytest
from app import (
    apis,
    models,
    configs,
)


@pytest.fixture
def client(request):
    _wsgi = apis.create_wsgi()
    config = configs.sqlalchemy.get_config('testing')
    config.SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    models.load_config_from_object(config)
    models.Base.metadata.create_all(bind=models.session.get_bind())
    with _wsgi.app.test_client() as _client:
        if request.cls is not None:
            request.cls.client = _client
        yield _client
