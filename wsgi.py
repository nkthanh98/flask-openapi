# coding=utf-8

import os
from app import (
    models,
    apis,
    sentry,
)


ENV = os.getenv('ENV', 'production')
application = apis.create_wsgi(ENV)
models.load_config(ENV)
sentry.load_and_start(ENV)
