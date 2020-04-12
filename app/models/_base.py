# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL


Base = declarative_base()        # pylint: disable=C0103
session = scoped_session(sessionmaker(      #pylint: disable=C0103
    autocommit=False,
    autoflush=False
))


def init_db(drive, credentials):
    engine = create_engine(         # pylint: disable=C0103
        URL(drive, **credentials),
        convert_unicode=True,
        echo=True
    )
    session.configure(bind=engine)
    Base.metadata.create_all(bind=engine)
