# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()        # pylint: disable=C0103
session = scoped_session(sessionmaker(      #pylint: disable=C0103
    autocommit=False,
    autoflush=False
))


def config_from_object(config):
    engine = create_engine(         # pylint: disable=C0103
        config.SQLALCHEMY_DATABASE_URI,
        convert_unicode=True,
        echo=False
    )
    session.configure(bind=engine)
