# coding=utf-8

from sqlalchemy import (
    Column,
    types,
    func,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from app import models


class User(models.Base):
    __tablename__ = 'users'

    id = Column(types.Integer(), primary_key=True, autoincrement=True)
    fullname = Column(types.String(50), nullable=False)
    username = Column(types.String(50), nullable=False, unique=True, index=True)
    password_hash = Column(types.String(128), nullable=False)
    is_active = Column(types.Boolean(), default=False, nullable=False)
    created_at = Column(types.TIMESTAMP, default=func.now())
    updated_at = Column(types.TIMESTAMP, onupdate=func.now())

    @property
    def password(self):
        raise ValueError('This is a only read attribute')

    @password.getter
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def verify_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)
