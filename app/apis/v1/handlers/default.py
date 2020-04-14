# coding=utf-8

from connexion import NoContent

def ping():
    raise Exception('Lol')
    return NoContent
