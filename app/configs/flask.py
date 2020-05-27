# coding=utf-8

from app import configs


class BaseConfig(configs.Config):
    pass


class DevelopmentConfig(BaseConfig):
   __name__ = 'development'

   TESTING = False
   DEBUG = True


class TestingConfig(BaseConfig):
    __name__ = 'testing'
    TESTING = True
    DEBUG = False


class ProductionConfig(BaseConfig):
   __name__ = 'production'

   TESTING = False
   DEBUG = False


def get_config(config_name):
    return {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
    }.get(config_name)
