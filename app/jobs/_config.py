# coding=utf-8

import os


broker_url = os.getenv('CELERY_BROKER_URL', 'pyamqp://')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'rpc://')

task_serializer = 'pickle'
result_serializer = 'pickle'
accept_content = ['pickle', 'json']
timezone = 'Europe/Oslo'
enable_utc = True
