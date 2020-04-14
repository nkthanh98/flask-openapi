# coding=utf-8

import os


broker_url = os.getenv('CELERY_BROKER_URL', 'pyamqp://')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'rpc://')
result_persistent = True if os.getenv('CELERY_RESULT_PERSISTENT', '1') == '1' else False

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Oslo'
enable_utc = True
