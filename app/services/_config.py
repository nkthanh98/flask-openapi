#coding=utf-8

import os


JWT_ALGORITHM = 'HS256'

JWT_KEY = os.getenv('JWT_KEY', 'secret')

LOGIN_TIME_ALIVE = int(os.getenv('LOGIN_TIME_ALIVE', str(60 * 60 * 24)))      # 1 day

ISSUE_MAINTAINER = os.getenv('ISSUE_MAINTAINER', 'admin@app.com')
