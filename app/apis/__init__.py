#coding=utf-8

import os
from flask_cors import CORS
from connexion import (
    FlaskApp,
    Resolver,
)
from app import models
from . import config


class VersionResolver(Resolver):
    def __init__(self, prefix):
        super().__init__()
        self._prefix = prefix

    def resolve_operation_id(self, operation):
        return f'{self._prefix}.{operation.operation_id}'


def create_wsgi():
    options = {
        'swagger_ui': True
    }
    if config.ENV == 'prod':
        options['swagger_ui'] = False
    application = FlaskApp(__name__, options=options)
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
