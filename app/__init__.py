# coding=utf-8

from connexion import (
    FlaskApp,
    Resolver,
)
from flask_cors import CORS
from . import config
from . import models
from . import utils
from . import repos
from . import services
from . import jobs


class VersionResolver(Resolver):
    def __init__(self, prefix):
        super().__init__()
        self._prefix = prefix

    def resolve_operation_id(self, operation):
        return f'{self._prefix}.{operation.operation_id}'


def create_app():
    application = FlaskApp(__name__, specification_dir='specs')

    application.add_api(
        specification='openapi-v1.yaml',
        resolver=VersionResolver('app.apis.v1.handlers'),
        strict_validation=True,
        validate_responses=True
    )

    models.init_db(config.DATABASE_DRIVE, config.DATABASE_CREDENTIALS)
    if config.ENVIRONMENT == 'production':
        def shutdown_session(exception):
            models.session.remove()
        application.app.teardown_appcontext(shutdown_session)
    CORS(application.app)

    return application
