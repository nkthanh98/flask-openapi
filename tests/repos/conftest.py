# coding=utf-8

import pytest
from app import models


@pytest.fixture
def db():
    models.init(
        drive='sqlite',
        credentials={
            'database': ':memory:'
        }
    )
    models.Base.metadata.create_all(bind=models.session.get_bind())
    yield models.session
