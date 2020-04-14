# coding=utf-8

from unittest.mock import patch
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
    yield models.session
