# coding=utf-8

import os
from app import configs


class BaseConfig(configs.Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


class DevelopmentConfig(BaseConfig):
    __name__ = 'development'


class TestingConfig(BaseConfig):
    __name__ = 'testing'


class ProductionConfig(BaseConfig):
    __name__ = 'production'


def get_config(config_name):
    return {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
    }.get(config_name)
