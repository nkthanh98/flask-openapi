# coding-utf-8

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from app import configs


def load_and_start(config_name):
    config = configs.sentry.get_config(config_name)
    sentry_sdk.init(
        dsn=config.DSN,
        integrations=[
            FlaskIntegration(),
            CeleryIntegration(),
            SqlalchemyIntegration()
        ]
    )
