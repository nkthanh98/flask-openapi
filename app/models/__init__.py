# coding=utf-8

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from ._base import (
    Base,
    engine,
)
from .task import Task
from .user import User


session = scoped_session(sessionmaker(      #pylint: disable=C0103
    bind=engine,
    autocommit=False,
    autoflush=False
))

Base.metadata.create_all(bind=engine)
