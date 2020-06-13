# coding=utf-8

import os
from sentry_sdk import init as sentry_init
from sentry_sdk.integrations import celery as sentry_celery
from celery import Celery
from . import config


manager = Celery('app')
manager.config_from_object(config)
sentry_init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=(sentry_celery.CeleryIntegration(),)
)
