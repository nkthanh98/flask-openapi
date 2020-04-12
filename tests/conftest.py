# coding=utf-8

import pytest
from app import (
    create_app,
    models,
)


@pytest.fixture
def db():
    models.init_db(
        drive='sqlite',
        credentials={
            'database': ':memory:'
        }
    )
    yield models.session


@pytest.fixture
def client(request):
    _app = create_app()
    with _app.app.test_client() as client:
        if request.cls is not None:
            request.cls.client = client
        yield client
