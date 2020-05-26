#coding=utf-8

import os


class Config:
    ROOT_DIR = os.path.abspath(os.getcwd())

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    SENTRY_DSN = os.getenv('SENTRY_DSN')

    ENV = os.getenv('ENV')
