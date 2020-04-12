# coding=utf-8

import pytest
from app import (
    create_app,
    models,
)


@pytest.fixture
def app():
    _app = create_app()
    ctx = _app.app.app_context()
    ctx.push()
    yield _app.app
    ctx.pop()


@pytest.fixture
@pytest.mark.usefixtures('app')
def app_class(request, app):
    if request.cls is not None:
        request.cls.app = app


@pytest.fixture
def db():
    models.init_db(
        drive='sqlite',
        credentials={
            'database': ':memory:'
        }
    )
    yield models.session
