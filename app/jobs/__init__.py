# coding=utf-8

from app import configs
from ._base import manager


manager.config_from_object(configs.celery)
