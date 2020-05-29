# coding=utf-8

import os
from app import configs


class DevelopmentConfig(configs.Config):
    __name__ = 'development'

    DSN = os.getenv('SENTRY_DNS')


class TestingConfig(configs.Config):
    __name__ = 'testing'


class ProductionConfig(configs.Config):
    __name__ = 'production'


def get_config(config_name):
    return {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
    }.get(config_name)
