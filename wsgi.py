# coding=utf-8

import os
import logging.config
from app import (
    models,
    apis,
    sentry,
)


logging.config.fileConfig('logging.ini')
ENV = os.getenv('ENV', 'production')
application = apis.create_wsgi(ENV)
models.load_config(ENV)
sentry.load_and_start(ENV)
