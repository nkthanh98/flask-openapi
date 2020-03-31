# coding=utf-8

import socket
import logging
from app.jobs import send_message_to_slack_channel


class SlackHandler(logging.Handler):
    HOSTNAME = socket.gethostname()

    def __init__(self, token, channel_id, run_async=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._run_async = run_async
        self._token = token
        self._channel_id = channel_id

    def emit(self, record):
        if self._run_async:
            caller = send_message_to_slack_channel.delay
        else:
            caller = send_message_to_slack_channel.apply
        caller(self._token, self._channel_id, self.format(record))

    def format(self, record):
        exc_cls, exc, _ = record.exc_info
        content = {
            'title': str(exc),
            'color': '#eb3b3b',
            'ts': int(record.created),
            'footer': self.HOSTNAME,
            'fields': [
                {
                    'title': 'Exception',
                    'value': exc_cls.__name__
                },
                {
                    'title': 'Traceback',
                    'value': super().format(record)
                }
            ]
        }
        return [content]
