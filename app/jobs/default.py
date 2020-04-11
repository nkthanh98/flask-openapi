#coding=utf-8

from app.jobs import manager


@manager.task
def ping(message):
    ret = f'Say {message}'
    print(ret)
    return ret
