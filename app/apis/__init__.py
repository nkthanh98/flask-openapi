#coding=utf-8

import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_cors import CORS
from connexion import (
    FlaskApp,
    Resolver,
)
from app import (
    models,
    configs,
)


class VersionResolver(Resolver):
    def __init__(self, prefix):
        super().__init__()
        self._prefix = prefix

    def resolve_operation_id(self, operation):
        return f'{self._prefix}.{operation.operation_id}'


def create_wsgi(config_name=None):
    application = FlaskApp(__name__)
    config_obj = configs.flask.get_config(config_name or application.app.env)
    application.app.config.from_object(config_obj)
    CORS(application.app)

    application.add_api(
        specification='v1/openapi.yaml',
        resolver=VersionResolver('app.apis.v1.handlers'),
        strict_validation=True,
        validate_responses=True
    )

    @application.app.teardown_appcontext
    def shutdown_session(exception):
        models.session.remove()

    sentry_sdk.init(
        dsn=config_obj.SENTRY_DSN,
        integrations=[FlaskIntegration()]
    )

    return application
