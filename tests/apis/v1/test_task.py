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
    access_token = auth.generate_access_token(user.username)
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
    access_token = auth.generate_access_token(user.username)
    task = models.Task(
        title=faker.name(),
        created_by=user.username
    )
    models.session.add(task)
    models.session.commit()
    url = f'/v1/tasks/{task.id}'
    res = client.get(url, headers={'Authorization': f'Bearer {access_token}'})
    assert res.status_code == 200, res.get_json()['detail']


def test_get_task_not_found(client):
    user = models.User(
        username=faker.name(),
        fullname=faker.name(),
        password=faker.text(16),
        is_active=True,
    )
    models.session.add(user)
    models.session.commit()
    access_token = auth.generate_access_token(user.username)
    url = f'/v1/tasks/{faker.random_int(100, 1000)}'
    res = client.get(url, headers={'Authorization': f'Bearer {access_token}'})
    assert res.status_code == 404


def test_get_task_owned_by_other_user(client):
    user1 = models.User(
        username=faker.name(),
        fullname=faker.name(),
        password=faker.text(16),
        is_active=True,
    )
    models.session.add(user1)
    user2 = models.User(
        username=faker.name(),
        fullname=faker.name(),
        password=faker.text(16),
    )
    models.session.add(user2)
    models.session.commit()
    access_token = auth.generate_access_token(user1.username)
    task = models.Task(
        title=faker.name(),
        created_by=user2.username
    )
    models.session.add(task)
    models.session.commit()
    url = f'/v1/tasks/{task.id}'
    res = client.get(url, headers={'Authorization': f'Bearer {access_token}'})
    assert res.status_code == 404


def test_update_task_not_found(client):
    user = models.User(
        username=faker.name(),
        fullname=faker.name(),
        password=faker.text(16),
        is_active=True,
    )
    models.session.add(user)
    models.session.commit()
    access_token = auth.generate_access_token(user.username)
    url = f'/v1/tasks/{faker.random_int(100, 1000)}'
    res = client.patch(
        url,
        json={'title': faker.name()},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert res.status_code == 404


def test_update_task_owned_by_other_user(client):
    user1 = models.User(
        username=faker.name(),
        fullname=faker.name(),
        password=faker.text(16),
        is_active=True,
    )
    models.session.add(user1)
    user2 = models.User(
        username=faker.name(),
        fullname=faker.name(),
        password=faker.text(16),
    )
    models.session.add(user2)
    models.session.commit()
    access_token = auth.generate_access_token(user1.username)
    task = models.Task(
        title=faker.name(),
        created_by=user2.username
    )
    models.session.add(task)
    models.session.commit()
    url = f'/v1/tasks/{task.id}'
    res = client.patch(
        url,
        json={'title': faker.name()},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert res.status_code == 404


def test_delete_task_not_found(client):
    user = models.User(
        username=faker.name(),
        fullname=faker.name(),
        password=faker.text(16),
        is_active=True,
    )
    models.session.add(user)
    models.session.commit()
    access_token = auth.generate_access_token(user.username)
    url = f'/v1/tasks/{faker.random_int(100, 1000)}'
    res = client.delete(
        url,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert res.status_code == 404


def test_delete_task_owned_by_other_user(client):
    user1 = models.User(
        username=faker.name(),
        fullname=faker.name(),
        password=faker.text(16),
        is_active=True,
    )
    models.session.add(user1)
    user2 = models.User(
        username=faker.name(),
        fullname=faker.name(),
        password=faker.text(16),
    )
    models.session.add(user2)
    models.session.commit()
    access_token = auth.generate_access_token(user1.username)
    task = models.Task(
        title=faker.name(),
        created_by=user2.username
    )
    models.session.add(task)
    models.session.commit()
    url = f'/v1/tasks/{task.id}'
    res = client.delete(
        url,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert res.status_code == 404


def test_get_tasks(client):
    user = models.User(
        username=faker.name(),
        fullname=faker.name(),
        password=faker.text(16),
        is_active=True,
    )
    models.session.add(user)
    models.session.commit()
    access_token = auth.generate_access_token(user.username)
    tasks = list()
    for _ in range(3):
        task = models.Task(
            title=faker.name(),
            created_by=user.username,
            description=faker.text()
        )
        models.session.add(task)
        tasks.append(task)
    models.session.commit()
    url = f'/v1/tasks'
    res = client.get(url, headers={'Authorization': f'Bearer {access_token}'})
    assert res.status_code == 200, res.get_json()['detail']
    task_list_resp = sorted(res.get_json()['items'], key=lambda x: x['id'])
    assert len(tasks) == len(task_list_resp)
    for task, task_resp in zip(tasks, task_list_resp):
        assert task.title == task_resp['title']
        assert task.created_by == task_resp['created_by']
        assert task.description == task_resp['description']
        assert task.status == task_resp['status']
        assert task.created_at.strftime('%d/%m/%Y %H:%M:%S') == task_resp['created_at']


def test_update_task(client):
    user = models.User(
        username=faker.name(),
        fullname=faker.name(),
        password=faker.text(16),
        is_active=True,
    )
    models.session.add(user)
    models.session.commit()
    access_token = auth.generate_access_token(user.username)
    task = models.Task(
        title=faker.name(),
        created_by=user.username
    )
    models.session.add(task)
    models.session.commit()
    before_updated_at = task.updated_at
    url = f'/v1/tasks/{task.id}'
    data = {
        'title': faker.name(),
        'description': faker.text(),
        'status': faker.random_element(('new', 'done', 'failure', 'doing'))
    }
    resp = client.patch(
        url,
        json=data,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert resp.status_code == 204
    assert task.updated_at != before_updated_at
    assert task.title == data['title']
    assert task.description == data['description']
    assert task.status == data['status']


def test_delete_task(client):
    user = models.User(
        username=faker.name(),
        fullname=faker.name(),
        password=faker.text(16),
        is_active=True,
    )
    models.session.add(user)
    models.session.commit()
    access_token = auth.generate_access_token(user.username)
    task = models.Task(
        title=faker.name(),
        created_by=user.username
    )
    models.session.add(task)
    models.session.commit()
    url = f'/v1/tasks/{task.id}'
    resp = client.delete(
        url,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert resp.status_code == 204
    assert not models.session.query(models.Task).get(task.id)
