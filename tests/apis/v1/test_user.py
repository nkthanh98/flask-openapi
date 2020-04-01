# coding=utf-8

from app import (
    models,
    auth,
)
from tests import faker


def test_create_user(client):
    url = '/v1/users'
    data = {
        'username': faker.name(),
        'password': faker.text(16),
        'fullname': faker.name()
    }
    res = client.post(url, json=data)
    assert res.status_code == 201
    user = models.session.query(models.User).filter(
        models.User.username == data['username']
    ).first()
    assert user and not user.is_active
    assert user.fullname == data['fullname']


def test_get_user_info(client):
    user = models.User(
        username=faker.name(),
        fullname=faker.name(),
        password=faker.text(16),
        is_active=True
    )
    models.session.add(user)
    models.session.commit()
    access_token = auth.generate_access_token(user.username)
    url = '/v1/users/info'
    resp = client.get(url, headers={'Authorization': f'Bearer {access_token}'})
    assert resp.status_code == 200


def test_login(client):
    url = '/v1/login'
    password = faker.text(16)
    user = models.User(
        fullname=faker.name(),
        username=faker.name(),
        password=password
    )
    models.session.add(user)
    models.session.commit()
    data = {
        'username': user.username,
        'password': password
    }
    res = client.post(url, json=data)
    assert res.status_code == 200, res.get_json().get('detail')
    assert user.is_active


def test_login_with_username_is_wrong(client):
    url = '/v1/login'
    password = faker.text(16)
    user = models.User(
        fullname=faker.name(),
        username=faker.name(),
        password=password
    )
    models.session.add(user)
    models.session.commit()
    data = {
        'username': user.username + faker.text(),
        'password': password
    }
    res = client.post(url, json=data)
    assert res.status_code == 400


def test_login_with_password_is_wrong(client):
    url = '/v1/login'
    password = faker.text(16)
    user = models.User(
        fullname=faker.name(),
        username=faker.name(),
        password=password
    )
    models.session.add(user)
    models.session.commit()
    data = {
        'username': user.username,
        'password': password + faker.text()
    }
    res = client.post(url, json=data)
    assert res.status_code == 400


def test_logout(client):
    password = faker.text(16)
    user = models.User(
        fullname=faker.name(),
        username=faker.name(),
        password=password
    )
    user.is_active = True
    models.session.add(user)
    models.session.commit()
    access_token = auth.generate_access_token(user.username)
    res = client.post('/v1/logout', headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert res.status_code == 204
    assert not user.is_active
