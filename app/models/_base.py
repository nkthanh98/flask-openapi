# coding=utf-8

import logging
import time
from sqlalchemy import (
    create_engine,
    event
)
from sqlalchemy.engine import Engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from sqlalchemy.ext.declarative import declarative_base
from app import configs


RUNTIME_LOGGER = logging.getLogger('sqlalchemy.runtime')
QUERY_TIME_THRESHOLD = 0

Base = declarative_base()        # pylint: disable=C0103
session = scoped_session(sessionmaker(      #pylint: disable=C0103
    autocommit=False,
    autoflush=False
))


def before_cursor_execute(conn, cursor, statement, params, context, execmany):      # pylint: disable=W0613,R0913
    conn.info.setdefault('query_start_time', []).append(time.time())


def after_cursor_execute(conn, cursor, statement, params, context, execmany):       # pylint: disable=W0613,R0913
    total = time.time() - conn.info['query_start_time'].pop(-1)
    if total > QUERY_TIME_THRESHOLD:
        RUNTIME_LOGGER.debug(f' SLOW QUERY: {total:.3f} '.center(80, '-'))
        RUNTIME_LOGGER.debug(f'Params: {params}')       # pylint: disable=W1202
        RUNTIME_LOGGER.debug(statement)


def enable_time_logging():
    RUNTIME_LOGGER.setLevel(logging.DEBUG)
    event.listens_for(Engine, 'before_cursor_execute')(before_cursor_execute)
    event.listens_for(Engine, 'after_cursor_execute')(after_cursor_execute)


def load_config(config_name):
    config = configs.sqlalchemy.get_config(config_name)
    load_config_from_object(config)
    if config.QUERY_TIME_LOGGING:
        enable_time_logging()


def load_config_from_object(config):
    engine = create_engine(         # pylint: disable=C0103
        config.SQLALCHEMY_DATABASE_URI,
        convert_unicode=True,
        echo=False
    )
    session.configure(bind=engine)
