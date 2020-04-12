# coding=utf-8

from unittest.mock import patch
from app import (
    models,
    auth,
)
from tests import (
    faker,
    APITestCase,
)


class GetUserInfoTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        user = models.User(
            username=faker.name(),
            fullname=faker.name(),
            password=faker.text(16),
            is_active=True
        )
        models.session.add(user)
        models.session.commit()
        access_token = auth.generate_access_token(user.username)
        self.user = user
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }

    @staticmethod
    def url():
        return '/v1/users/info'

    @staticmethod
    def method():
        return 'GET'

    def test_get_user_info(self):
        with patch('app.services.get_user_info') as mock_get_user:
            mock_get_user.return_value = self.user
            body, http_code = self.call_api(headers=self.headers)
        assert http_code == 200
        assert body['username'] == self.user.username
        assert body['fullname'] == self.user.fullname


class UserLoginTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        raw_pass = faker.text(16)
        user = models.User(
            username=faker.name(),
            fullname=faker.name(),
            password=raw_pass,
            is_active=False
        )
        models.session.add(user)
        models.session.commit()
        self.user = user
        self.data = {
            'username': user.username,
            'password': raw_pass
        }

    @staticmethod
    def url():
        return '/v1/login'

    @staticmethod
    def method():
        return 'POST'

    def test_login(self):
        _, http_code = self.call_api(json=self.data)
        assert http_code == 200
        assert self.user.is_active

    def test_login_with_password_is_wrong(self):
        self.data['password'] = self.data['password'] + faker.text(5)
        _, http_code = self.call_api(json=self.data)
        assert http_code == 400
        assert not self.user.is_active

    def test_login_with_username_is_wrong(self):
        self.data['username'] = self.data['username'] + faker.text(5)
        _, http_code = self.call_api(json=self.data)
        assert http_code == 400
        assert not self.user.is_active


class UserLogoutTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        user = models.User(
            username=faker.name(),
            fullname=faker.name(),
            password=faker.text(16),
            is_active=True
        )
        models.session.add(user)
        models.session.commit()
        self.user = user
        access_token = auth.generate_access_token(user.username)
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }

    @staticmethod
    def url():
        return '/v1/logout'

    @staticmethod
    def method():
        return 'POST'

    def test_logout(self):
        _, http_code = self.call_api(headers=self.headers)
        assert http_code == 204
        assert not self.user.is_active


class CreateUserTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.data = {
            'username': faker.lexify('?'*16),
            'password': faker.lexify('?'*16),
            'fullname': faker.lexify('?'*16)
        }

    @staticmethod
    def url():
        return '/v1/users'

    @staticmethod
    def method():
        return 'POST'

    def test_create_user(self):
        _, http_code = self.call_api(json=self.data)
        assert http_code == 201
        user = models.session.query(models.User).filter(
            models.User.username == self.data['username']
        ).first()
        assert user and not user.is_active
        assert user.fullname == self.data['fullname']
