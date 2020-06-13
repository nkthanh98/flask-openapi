# coding=utf-

import os
import inspect


class BaseSettings:
    @classmethod
    def load(cls, **kwargs):
        attrs = inspect.getmembers(
            cls,
            lambda x: inspect.isdatadescriptor(x) and not x.__name__.startswith('_')
        )
        ret = cls()
        for name, dtype in attrs:
            if name in kwargs:
                setattr(ret, name, kwargs[name])
            else:
                env = os.getenv(name)
                if env:
                    setattr(ret, name, dtype(env))
                else:
                    setattr(ret, name, getattr(cls, name))
        return ret



class FlaskSettings(BaseSettings):
    DEBUG: int = 0
    TESTING: int = 0


class SQLAlchemySettings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///:memory:'
    QUERY_TIME_LOGGING: int = 0
    QUERY_TIME_THRESHOLD: float = 0.05
    SQLALCHEMY_ENGINE_LOG: int = 0


class SentrySetting(BaseSettings):
    SENTRY_DSN: str = ''


def load_config(config_class: list, **kwargs) -> BaseSettings:
    concrete_class = type("ConcreteSetting", config_class, {})
    return concrete_class.load(**kwargs)
