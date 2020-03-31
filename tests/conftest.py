# coding=utf-8

import pytest
from app import (
    create_app,
    models,
)


@pytest.fixture(scope='function')
def client():
    _app = create_app()
    yield _app.app.test_client()
    models.session.remove()
