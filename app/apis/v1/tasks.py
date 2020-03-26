# coding=utf-8

from werkzeug.exceptions import (
    BadRequest,
)
from connexion import (
    request,
    context,
)
from app.models import (
    Task,
    session,
)


def create_task():
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        description=data['description'],
        created_by=context['current_user'].username
    )
    session.add(new_task)
    session.commit()
    return {
        'id': new_task.id
    }, 201


def get_task(task_id):
    task = session.query(Task).filter(
        Task.id == task_id
    ).one_or_none()
    if task:
        return task.dump()
    return None


def get_tasks():
    tasks = session.query(Task).filter(
        Task.created_by == context['current_user'].username
    )
    return [task.dump() for task in tasks]


def update_task(task_id):
    task = session.query(Task).filter(
        Task.id == task_id
    ).one_or_none()
    if not task:
        raise BadRequest('Task not found')
    task.update(data=request.get_json())
    session.commit()
    return task.dump()


def delete_task(task_id):
    session.query(Task).filter(
        Task.id == task_id,
        Task.created_by == context['current_user'].username
    ).delete()
    session.commit()
