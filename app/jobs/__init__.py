# coding=utf-8

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from app import configs
from ._base import manager


manager.config_from_object(configs.celery)
sentry_sdk.init(
    dsn='',
    integrations=[CeleryIntegration()]
)
