#coding=utf-8

import os
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
    config = configs.flask.get_config(config_name)
    application.app.config.from_object(config)
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

    return application
