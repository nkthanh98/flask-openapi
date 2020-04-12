# coding=utf-8

import pytest
from app import models


@pytest.fixture
def db():
    models.init_db(
        drive='sqlite',
        credentials={
            'database': ':memory:'
        }
    )
    yield models.session
