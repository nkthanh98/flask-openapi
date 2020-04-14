# coding=utf-8

from app import (
    config,
    create_app,
    models,
    loggers,
)


application = create_app()

models.init(config.DATABASE_DRIVE, config.DATABASE_CREDENTIALS)

loggers.init('logging.ini', config.SLACK_BOT_TOKEN, config.SLACK_LOG_CHANNEL_ID)
