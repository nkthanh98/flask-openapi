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


class CreateTaskTestCase(APITestCase):
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
        self.data = {
            'title': faker.text(20),
        }
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }

    @staticmethod
    def url():
        return '/v1/tasks'

    @staticmethod
    def method():
        return 'POST'

    def test_create_task(self):
        body, http_code = self.call_api(json=self.data, headers=self.headers)
        assert http_code == 201
        task = models.session.query(
            models.Task
        ).get(body['id'])
        assert task
        assert task.title == self.data['title']
        assert not task.description


class GetTaskByIdTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        user = models.User(
            username=faker.name(),
            fullname=faker.name(),
            password=faker.text(16),
            is_active=True
        )
        models.session.add(user)
        models.session.flush()
        task = models.Task(
            title=faker.name(),
            created_by=user.username
        )
        models.session.add(task)
        models.session.commit()
        self.user = user
        self.task = task
        access_token = auth.generate_access_token(user.username)
        self.data = {
            'title': faker.text(20),
        }
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }

    @staticmethod
    def url():
        return '/v1/tasks/{}'

    @staticmethod
    def method():
        return 'GET'

    def test_get_task_by_id(self):
        url = self.url().format(self.task.id)
        with patch('app.services.get_task_for_user') as mock_get_task_for_user:
            mock_get_task_for_user.return_value = self.task
            _, http_code = self.call_api(url, headers=self.headers)
        assert http_code == 200


    def test_get_task_not_found(self):
        url = self.url().format(faker.random_int(100, 1000))
        with patch('app.services.get_task_for_user') as mock_get_task_for_user:
            mock_get_task_for_user.return_value = None
            _, http_code = self.call_api(url=url, headers=self.headers)
        assert http_code == 404


    def test_get_task_owned_by_other_user(self):
        url = self.url().format(self.task.id)
        with patch('app.services.get_task_for_user') as mock_get_task_for_user:
            mock_get_task_for_user.return_value = None
            _, http_code = self.call_api(url, headers=self.headers)
        assert http_code == 404


class UpdateTaskTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        user = models.User(
            username=faker.name(),
            fullname=faker.name(),
            password=faker.text(16),
            is_active=True
        )
        models.session.add(user)
        models.session.flush()
        task = models.Task(
            title=faker.name(),
            created_by=user.username
        )
        models.session.add(task)
        models.session.commit()
        self.user = user
        self.task = task
        access_token = auth.generate_access_token(user.username)
        self.data = {
            'title': faker.text(20),
        }
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }

    @staticmethod
    def url():
        return '/v1/tasks/{}'

    @staticmethod
    def method():
        return 'PATCH'

    def test_update_task_not_found(self):
        url = self.url().format(faker.random_int(100, 1000))
        with patch('app.services.update_task') as mock_update_task:
            mock_update_task.return_value = None
            _, http_code = self.call_api(url, json={'title': faker.text(20)},
                                         headers=self.headers)
        assert http_code == 404


    def test_update_task_owned_by_other_user(self):
        url = self.url().format(self.task.id)
        with patch('app.services.update_task') as mock_update_task:
            mock_update_task.return_value = None
            _, http_code = self.call_api(url, json={'title': faker.text(20)},
                                         headers=self.headers)
        assert http_code == 404

    def test_update_task(self):
        url = self.url().format(self.task.id)
        data = {
            'title': faker.name(),
            'description': faker.text(),
            'status': faker.random_element(('new', 'done', 'failure', 'doing'))
        }
        before_updated_at = self.task.updated_at
        _, http_code = self.call_api(url, json=data, headers=self.headers)
        assert http_code == 204
        assert self.task.updated_at != before_updated_at
        assert self.task.title == data['title']
        assert self.task.description == data['description']
        assert self.task.status == data['status']


class DeleteTaskTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        user = models.User(
            username=faker.name(),
            fullname=faker.name(),
            password=faker.text(16),
            is_active=True
        )
        models.session.add(user)
        models.session.flush()
        task = models.Task(
            title=faker.name(),
            created_by=user.username
        )
        models.session.add(task)
        models.session.commit()
        self.user = user
        self.task = task
        access_token = auth.generate_access_token(user.username)
        self.data = {
            'title': faker.text(20),
        }
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }

    @staticmethod
    def url():
        return '/v1/tasks/{}'

    @staticmethod
    def method():
        return 'DELETE'

    def test_delete_task_not_found(self):
        url = self.url().format(faker.random_int(100, 1000))
        _, http_code = self.call_api(url, headers=self.headers)
        assert http_code == 404


    def test_delete_task_owned_by_other_user(self):
        url = self.url().format(self.task.id)
        with patch('app.services.delete_task') as mock_delete_task:
            mock_delete_task.return_value = None
            _, http_code = self.call_api(url, headers=self.headers)
        assert http_code == 404

    def test_delete_task(self):
        url = self.url().format(self.task.id)
        _, http_code = self.call_api(url, headers=self.headers)
        assert http_code == 204
        assert not models.session.query(models.Task).get(self.task.id)


class GetListTaskTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        user = models.User(
            username=faker.name(),
            fullname=faker.name(),
            password=faker.text(16),
            is_active=True
        )
        models.session.add(user)
        models.session.flush()
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
        self.user = user
        self.tasks = tasks
        access_token = auth.generate_access_token(user.username)
        self.data = {
            'title': faker.text(20),
        }
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }

    @staticmethod
    def url():
        return '/v1/tasks'

    @staticmethod
    def method():
        return 'GET'

    def test_get_tasks(self):
        with patch('app.services.get_tasks_for_user') as mock_get_tasks_for_user:
            mock_get_tasks_for_user.return_value = self.tasks, len(self.tasks)
            body, http_code = self.call_api(headers=self.headers)
        assert http_code == 200
        task_list_resp = sorted(body['items'], key=lambda x: x['id'])
        assert len(self.tasks) == len(task_list_resp)
        for task, task_resp in zip(self.tasks, task_list_resp):
            assert task.title == task_resp['title']
            assert task.created_by == task_resp['created_by']
            assert task.description == task_resp['description']
            assert task.status == task_resp['status']
            assert task.created_at.strftime('%d/%m/%Y %H:%M:%S') == task_resp['created_at']
