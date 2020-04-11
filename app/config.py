# coding=utf-8

import os


ENVIRONMENT = os.getenv('ENVIRONMENT', 'testing')

JWT_ALGORITHM = 'HS256'

JWT_KEY = os.getenv('JWT_KEY', 'secret')

LOGIN_TIME_ALIVE = int(os.getenv('LOGIN_TIME_ALIVE', str(60 * 60 * 24)))      # 1 day

DATABASE_DRIVE = os.getenv('DB_DRIVE', 'sqlite')

DATABASE_CREDENTIALS = {
    'username': os.getenv('DB_USER', None),
    'password': os.getenv('DB_PASS', None),
    'host': os.getenv('DB_HOST', None),
    'port': os.getenv('DB_PORT', None),
    'database': os.getenv('DB_NAME', ':memory:')
}


ISSUE_MAINTAINER = os.getenv('ISSUE_MAINTAINER', 'nkthanh.uet@gmail.com')
