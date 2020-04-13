# coding=utf-8

import logging.config
from .formatters import (
    Formatter,
    SlackFormatter
)
from .handlers import (
    SlackHandler,
)


def init(config_file=None, slack_token=None, slack_channel_id=None):
    if config_file is not None:
        defaults = {}
        if slack_token is not None:
            defaults['token'] = slack_token
        if slack_channel_id is not None:
            defaults['channel_id'] = slack_channel_id
        logging.config.fileConfig(
            fname=config_file,
            defaults=defaults
        )
