# coding=utf-8

from app import (
    models,
    loggers,
    apis,
)


application = apis.create_wsgi()

models.init(apis.config.DATABASE_DRIVE, apis.config.DATABASE_CREDENTIALS)

loggers.init('logging.ini', apis.config.SLACK_BOT_TOKEN, apis.config.SLACK_LOG_CHANNEL_ID)
