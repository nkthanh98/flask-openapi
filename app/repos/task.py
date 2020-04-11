# coding=utf-8

import six
from sqlalchemy import exc
from app import models


def create_task(title, created_by, description=None, status='new'):
    try:
        new_task = models.Task(
            title=title,
            created_by=created_by,
            description=description,
            status=status,
        )
        models.session.add(new_task)
        models.session.commit()
    except exc.IntegrityError as db_error:
        raise six.raise_from(
            value=ValueError(f'User {created_by} not exist'),
            from_value=db_error
        )
    else:
        return new_task


def get_task_by_id(task_id):
    return models.session.query(models.Task).get(task_id)


def update_task(task_id_or_task, data):
    if isinstance(task_id_or_task, int):
        task = get_task_by_id(task_id_or_task)
    else:
        task = task_id_or_task

    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        task.status = data['status']

    models.session.commit()
    return task


def get_tasks_with_filters(filters, page=1, per_page=10):
    query = models.session.query(models.Task)

    if 'title' in filters:
        query = query.filter(
            models.Task.title.like(f'%{filters["title"]}%')
        )
    if 'status' in filters:
        query = query.filter(
            models.Task.status == filters.status
        )

    total_item = query.count()
    query = query.offset((page - 1) * per_page).limit(per_page)
    return query, total_item


def delete_task(task_id_or_task):
    if isinstance(task_id_or_task, int):
        models.session.query(models.Task).get(task_id_or_task).delete()
    else:
        models.session.delete(task_id_or_task)
    models.session.commit()
