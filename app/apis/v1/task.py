# coding=utf-8

from werkzeug import exceptions as exc
from connexion import (
    request,
    context,
    NoContent,
)
from app import repos


def create_task():
    data = request.get_json()
    new_task = repos.create_task(
        title=data['title'],
        description=data.get('description'),
        created_by=context['current_user'].username
    )
    return {
        'id': new_task.id
    }, 201


def get_task(task_id):
    task = repos.get_task_by_id(task_id)
    if not task:
        raise exc.BadRequest('Task not found')
    if task.created_by != context['current_user'].username:
        raise exc.Forbidden()
    return task.dump()


def get_tasks():
    tasks = repos.get_tasks_with_filters({
        'created_by': context['current_user'].username,
    })
    return [task.dump() for task in tasks]


def update_task(task_id):
    task = repos.get_task_by_id(task_id)
    if not task:
        raise exc.BadRequest('Task not found')
    if task.created_by != context['current_user'].username:
        raise exc.Forbidden()
    repos.update_task(task, request.get_json())
    return NoContent


def delete_task(task_id):
    task = repos.get_task_by_id(task_id)
    if not task:
        raise exc.BadRequest('Task not found')
    if task.created_by != context['current_user'].username:
        raise exc.Forbidden()
    repos.delete_task(task)
    return NoContent
