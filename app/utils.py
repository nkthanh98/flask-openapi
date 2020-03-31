#coding=utf-8

from marshmallow import Schema


def dump(schema_cls: Schema, data: dict, **options):
    schema = schema_cls(**options)
    return schema.dump(data)
