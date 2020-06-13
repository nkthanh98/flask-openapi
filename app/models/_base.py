# coding=utf-8

import logging
import time
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from sqlalchemy.ext.declarative import declarative_base


RUNTIME_LOGGER = logging.getLogger('sqlalchemy.runtime')

Base = declarative_base()        # pylint: disable=C0103
session = scoped_session(sessionmaker(      #pylint: disable=C0103
    autocommit=False,
    autoflush=False
))



def enable_time_logging(query_time_threshold):
    def before_cursor_execute(conn, cursor, statement, params, context, execmany):      # pylint: disable=W0613,R0913
        conn.info.setdefault('query_start_time', []).append(time.time())


    def after_cursor_execute(conn, cursor, statement, params, context, execmany):       # pylint: disable=W0613,R0913
        total = time.time() - conn.info['query_start_time'].pop(-1)
        if total > query_time_threshold:
            RUNTIME_LOGGER.debug(f' SLOW QUERY: {total:.3f} '.center(80, '-'))
            RUNTIME_LOGGER.debug(f'Params: {params}')       # pylint: disable=W1202
            RUNTIME_LOGGER.debug(statement)

    RUNTIME_LOGGER.setLevel(logging.DEBUG)
    event.listens_for(Engine, 'before_cursor_execute')(before_cursor_execute)
    event.listens_for(Engine, 'after_cursor_execute')(after_cursor_execute)
