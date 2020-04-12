#coding=utf-8

import unittest
import pytest
from faker import (
    Factory,
    Faker,
)
from flask.testing import FlaskClient


faker = Factory.create()


class BaseTestCase(unittest.TestCase):
    KEY: str = None


@pytest.mark.usefixtures('client')
class APITestCase(BaseTestCase):
    client: FlaskClient = None

    @staticmethod
    def url():
        return NotImplemented

    @staticmethod
    def method():
        return NotImplemented

    def call_api(self, url=None, method=None, json=None, headers=None):
        method = (method or self.method()).lower()
        url = url or self.url()
        assert method in ('get', 'put', 'patch', 'post', 'delete'), f'{method} not support'
        caller = getattr(self.client, method)
        if method == 'get':
            resp = caller(url, headers=headers)
        else:
            resp = caller(url, json=json, headers=headers)
        body = None
        if resp.content_length and resp.is_json:
            body = resp.get_json()
        else:
            body = resp.get_data(as_text=True)
        return body, resp.status_code


class ServiceTestCase(BaseTestCase):
    pass


class RepositoryTestCase(BaseTestCase):
    pass


class JobTestCase(BaseTestCase):
    pass
