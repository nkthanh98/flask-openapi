# coding=utf-8

from connexion import (
    FlaskApp,
    Resolver,
)
from . import config
from . import models


class VersionResolver(Resolver):
    def __init__(self, prefix):
        super().__init__()
        self._prefix = prefix

    def resolve_operation_id(self, operation):
        return '{}.{}'.format(self._prefix, operation.operation_id)


def create_app():
    app = FlaskApp(__name__, specification_dir='specs')

    app.add_api(
        specification='openapi-v1.yaml',
        base_path='/v1',
        resolver=VersionResolver('app.apis.v1'),
        strict_validation=True
    )

    return app
