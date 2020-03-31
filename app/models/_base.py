# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from app import config

session = None

class ModelBaseExtend:
    def dump(self, exclude_fields=None, include_fields=None):
        if include_fields:
            dump_fields = include_fields
        else:
            dump_fields = self.__dict__.keys()
        exclude_fields = list() if exclude_fields is None else exclude_fields
        dump_fields = filter(lambda x: not x.startswith('_'))
        ret = {}
        for field_name in dump_fields:
            if field_name in exclude_fields:
                continue
            field_value = getattr(self, field_name)
            if hasattr(field_name, 'dump'):
                ret[field_name] = getattr(field_value, 'dump')()
            else:
                ret[field_name] = field_value
        return ret

    def update(self, data, ignore_error=True, ignore_none=True):
        for key, value in data.items():
            if hasattr(self, key):
                if value is None and ignore_none:
                    continue
                setattr(self, key, value)
            else:
                if not ignore_error:
                    raise AttributeError(
                        f'Can\'t not set {key} to {self.__class__.__name__} class'
                    )

Base = declarative_base(cls=ModelBaseExtend)        # pylint: disable=C0103

session = scoped_session(sessionmaker(      #pylint: disable=C0103
    autocommit=False,
    autoflush=False
))


def init_db():
    engine = create_engine(         # pylint: disable=C0103
        URL(config.DATABASE_DRIVE, **config.DATABASE_CREDENTIALS),
        convert_unicode=True,
        echo=True
    )
    session.configure(bind=engine)
    Base.metadata.create_all(bind=engine)
