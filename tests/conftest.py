# coding=utf-8

from unittest.mock import patch
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


@pytest.fixture
def slack_mock():
    with patch('app.jobs.send_message_to_slack_channel.delay') as mock:
        yield mock
