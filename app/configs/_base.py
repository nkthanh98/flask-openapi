# coding=utf-8

import os


class Config:
    __name__ = None

    ROOT_DIR = os.path.abspath(os.getcwd())

    SENTRY_DSN = os.getenv('SENTRY_DSN')
