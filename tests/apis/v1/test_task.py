# coding=utf-8

from app import (
    models,
    auth,
)
from tests import faker


def test_create_task(client):
    url = '/v1/tasks'
    user = models.User(
        username=faker.name(),
        fullname=faker.name(),
        password=faker.text(16),
        is_active=True
    )
    models.session.add(user)
    models.session.commit()
    access_token = auth.generate_access_token({
        'username': user.username
    })
    data = {
        'title': faker.text(20),
    }
    res = client.post(
        url,
        json=data,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert res.status_code == 201, res.get_json()
    task = models.session.query(
        models.Task
    ).get(res.get_json()['id'])
    assert task
    assert task.title == data['title']
    assert not task.description


def test_get_task_by_id(client):
    user = models.User(
        username=faker.name(),
        fullname=faker.name(),
        password=faker.text(16),
        is_active=True,
    )
    models.session.add(user)
    models.session.commit()
    access_token = auth.generate_access_token({
        'username': user.username
    })
    task = models.Task(
        title=faker.name(),
        created_by=user.username
    )
    models.session.add(task)
    models.session.commit()
    url = f'/v1/tasks/{task.id}'
    res = client.get(url, headers={'Authorization': f'Bearer {access_token}'})
    assert res.status_code == 200, res.get_json()['detail']
