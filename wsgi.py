# coding=utf-8

from app import (
    models,
    apis,
    configs,
)


application = apis.create_wsgi()

models.config_from_object(configs.sqlalchemy)
