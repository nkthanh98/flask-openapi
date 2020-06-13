# coding=utf-8

import os
from sentry_sdk import init as sentry_init
from sentry_sdk.integrations import flask as sentry_flask
from flask_cors import CORS
from connexion import (
    FlaskApp,
    Resolver,
)
from app import (
    models,
    settings,
)


class VersionResolver(Resolver):
    def __init__(self, prefix):
        super().__init__()
        self._prefix = prefix

    def resolve_operation_id(self, operation):
        return f'{self._prefix}.{operation.operation_id}'


def create_wsgi():
    application = FlaskApp(__name__)
    config = settings.load_config(
        (settings.FlaskSettings, settings.SentrySetting,)
    )
    application.app.config.from_object(config)
    CORS(application.app)

    application.add_api(
        specification='v1/openapi.yaml',
        resolver=VersionResolver('app.http.v1.handlers'),
        strict_validation=True,
        validate_responses=True
    )

    @application.app.teardown_appcontext
    def shutdown_session(exception):
        models.session.remove()

    sentry_init(
        dsn=config.SENTRY_DSN,
        integrations=[sentry_flask.FlaskIntegration()]
    )

    return application
