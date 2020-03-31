# coding=utf-8
"""
Logging extension
"""

import inspect
import traceback as tb
from logging import Formatter as BaseFormatter


class Formatter(BaseFormatter):
    """Formatter
    Format exception logging follow
    [lineno] [filename]
             [line]
    """
    def formatException(self, exc_info): # pylint:disable=W0221
        exc_type, exc, traceback = exc_info
        result = inspect.cleandoc(
            f'''
            Exception: {exc_type.__name__}
            Message  : {str(exc)}
            '''
        )
        for item in tb.extract_tb(traceback):
            result = f'{result}\n{item.lineno:<6} {item.filename:} \n\t{item.line}'
        return result


class SlackFormatter(BaseFormatter):
    """Formatter
    Format exception logging follow
    [lineno] [filename]
             [line]
    """
    def formatException(self, exc_info): # pylint:disable=W0221
        exc_type, exc, traceback = exc_info
        result = ''
        for item in tb.extract_tb(traceback):
            result = f'{result}\n*{item.lineno:<6}* {item.filename:} \n\t{item.line}'
        return result
