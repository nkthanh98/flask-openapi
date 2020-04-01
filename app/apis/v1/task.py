# coding=utf-8

from werkzeug import exceptions as exc
from connexion import (
    request,
    NoContent,
)
from app import (
    repos,
    utils,
)
from . import task_schema


def create_task(user):
    data = request.get_json()
    new_task = repos.create_task(
        title=data['title'],
        description=data.get('description'),
        created_by=user
    )
    return {
        'id': new_task.id
    }, 201


def get_task(task_id, user):
    task = repos.get_task_by_id(task_id)
    if not task:
        raise exc.NotFound()
    if task.created_by != user:
        raise exc.Forbidden()
    return utils.dump(task_schema.Task, task)


def get_tasks(user):
    tasks = repos.get_tasks_with_filters({
        'created_by': user
    })
    return utils.dump(task_schema.Task, tasks, many=True)

def update_task(task_id, user):
    task = repos.get_task_by_id(task_id)
    if not task:
        raise exc.NotFound()
    if task.created_by != user:
        raise exc.Forbidden()
    repos.update_task(task, request.get_json())
    return NoContent


def delete_task(task_id, user):
    task = repos.get_task_by_id(task_id)
    if not task:
        raise exc.NotFound()
    if task.created_by != user:
        raise exc.Forbidden()
    repos.delete_task(task)
    return NoContent
