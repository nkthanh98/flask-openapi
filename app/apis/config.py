# coding=utf-8

import os


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

ENV = os.getenv('ENV', 'dev')

DATABASE_DRIVE = os.getenv('DB_DRIVE', 'sqlite')

DATABASE_CREDENTIALS = {
    'username': os.getenv('DB_USER', None),
    'password': os.getenv('DB_PASS', None),
    'host': os.getenv('DB_HOST', None),
    'port': os.getenv('DB_PORT', None),
    'database': os.getenv('DB_NAME', ':memory:')
}

LOG_FILE = os.getenv('LOG_FILE', '/tmp/app')

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN', '')

SLACK_LOG_CHANNEL_ID = os.getenv('SLACK_LOG_CHANNEL_ID', '')
