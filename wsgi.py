# coding=utf-8

from app import (
    config,
    models,
    loggers,
    apis,
)


application = apis.create_wsgi()

models.init(config.DATABASE_DRIVE, config.DATABASE_CREDENTIALS)

loggers.init('logging.ini', config.SLACK_BOT_TOKEN, config.SLACK_LOG_CHANNEL_ID)
