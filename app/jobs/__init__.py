# coding=utf-8

from ._base import manager
from . import _config
from .default import ping


manager.config_from_object(_config)
