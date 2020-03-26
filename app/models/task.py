# coding=utf-8

from sqlalchemy import (
    Column,
    types,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from app import models


class Task(models.Base):
    __tablename__ = 'tasks'

    id = Column(types.Integer(), primary_key=True, autoincrement=True)
    title = Column(types.String(50), nullable=False)
    description = Column(types.String(255))
    status = Column(types.String(20), nullable=False, default='new')
    created_by = Column(types.String(), ForeignKey('users.username'),
                        nullable=False)
    owner = relationship('User', backref='tasks')
    created_at = Column(types.TIMESTAMP, default=func.now())
    updated_at = Column(types.TIMESTAMP, onupdate=func.now())

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.title}>'
