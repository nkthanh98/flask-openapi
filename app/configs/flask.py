# coding=utf-8

from app.configs import Config as BaseConfig


class DevelopmentConfig(BaseConfig):
   TESTING = False
   DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = False


class ProductionConfig(BaseConfig):
   TESTING = False
   DEBUG = False


def get_config(config_name):
    return {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
    }.get(config_name)
