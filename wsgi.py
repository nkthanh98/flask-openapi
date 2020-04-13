# coding=utf-8

from app import (
    create_app,
    models,
    config,
    loggers,
)


application = create_app()

models.init_db(config.DATABASE_DRIVE, config.DATABASE_CREDENTIALS)

loggers.init('logging.ini', config.SLACK_BOT_TOKEN, config.SLACK_LOG_CHANNEL_ID)
