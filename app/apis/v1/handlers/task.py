# coding=utf-8

from werkzeug import exceptions as exc
from connexion import (
    request,
    NoContent,
)
from app import (
    services,
    utils,
)
from ..schemas import task as task_schema


def create_task(user):
    data = request.get_json()
    new_task = services.create_task(user, data)
    return {
        'id': new_task.id
    }, 201


def get_task(task_id, user):
    task = services.get_task_for_user(user, task_id)
    if not task:
        raise exc.NotFound()
    if task.created_by != user:
        raise exc.NotFound()
    return utils.dump(task_schema.Task, task)


def get_tasks(user):
    page = request.args.get('page', 1)
    page_size = request.args.get('page_size', 10)
    tasks, total_item = services.get_tasks_for_user(user, None, page, page_size)
    return {
        'items': utils.dump(task_schema.Task, tasks, many=True),
        'total_item': total_item,
        'page': page,
        'page_size': page_size
    }


def update_task(task_id, user):
    updated_task = services.update_task(task_id, user, request.get_json())
    if not updated_task:
        raise exc.NotFound()
    return NoContent


def delete_task(task_id, user):
    deleted_task = services.delete_task(task_id, user)
    if not deleted_task:
        raise exc.NotFound()
    return NoContent
