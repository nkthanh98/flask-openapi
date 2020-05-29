# coding=utf-8

import pytest
from app import (
    models,
    configs,
)


@pytest.fixture
def db():
    config = configs.sqlalchemy.get_config('testing')
    config.SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    models.load_config_from_object(config)
    models.Base.metadata.create_all(bind=models.session.get_bind())
    yield models.session
