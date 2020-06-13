# coding=utf-8

from marshmallow import (
    Schema,
    fields,
)


class Task(Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    status = fields.String()
    created_by = fields.String()
    created_at = fields.DateTime(format='%d/%m/%Y %H:%M:%S')
