# coding-utf-8

import sentry_sdk
from sentry_sdk import integrations
from app import configs


def load_and_start(config_name):
    config = configs.sentry.get_config(config_name)
    sentry_sdk.init(
        dsn=config.DSN,
        integrations=[
            integrations.flask.FlaskIntegration(),
            integrations.celery.CeleryIntegration(),
            integrations.sqlalchemy.SqlalchemyIntegration()
        ]
    )
