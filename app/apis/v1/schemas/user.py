# coding=utf-8

from marshmallow import (
    Schema,
    fields,
)


class User(Schema):
    id = fields.Integer()
    username = fields.String()
    fullname = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
