#coding=utf-8

from app.jobs import manager
from app import models


@manager.task(serializer='json')
def ping(message):
    ret = f'Say {message}'
    ret = models.session.query(models.Task).count()
    return ret
