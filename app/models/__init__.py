# coding=utf-8

from sentry_sdk import init as sentry_init
from sentry_sdk.integrations import sqlalchemy as sentry_sqlalchemy
from sqlalchemy.engine import create_engine
from app import settings
from ._base import (
    Base,
    session,
    enable_time_logging,
)
from .task import Task
from .user import User


config = settings.load_config(
    (settings.SQLAlchemySettings, settings.SentrySetting,)
)
if config.QUERY_TIME_LOGGING:
    enable_time_logging(config.QUERY_TIME_THRESHOLD)

engine = create_engine(         # pylint: disable=C0103
    config.SQLALCHEMY_DATABASE_URI,
    convert_unicode=True,
    echo=bool(config.SQLALCHEMY_ENGINE_LOG)
)
session.configure(bind=engine)

sentry_init(
    dsn=config.SENTRY_DSN,
    integrations=(sentry_sqlalchemy.SqlalchemyIntegration(),)
)
