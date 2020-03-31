# coding=utf-8

from ._base import manager
from . import _config
from .notify import send_message_to_slack_channel


manager.config_from_object(_config)
