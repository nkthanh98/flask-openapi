# coding=utf-8

from app import (
    create_app,
    models,
    config,
)


application = create_app()

models.init_db(config.DATABASE_DRIVE, config.DATABASE_CREDENTIALS)

_flask_app = application.app
