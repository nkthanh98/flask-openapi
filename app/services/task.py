# coding=utf-8

from app import repos

def get_tasks_for_user(user, filters=None, page=1, per_page=10):
    filters = filters or {}
    filters.update({'created_by': user})
    return repos.get_tasks_with_filters(filters, page, per_page)


def get_task_for_user(user, task_id):
    task = repos.get_task_by_id(task_id)
    return task if task and task.created_by == user else None


def create_task(user, data):
    return repos.create_task(
        title=data['title'],
        description=data.get('description'),
        status='new',
        created_by=user
    )


def update_task(task_id, user, data):
    task = repos.get_task_by_id(task_id)
    if not task or task.created_by != user:
        return None
    repos.update_task(task, data)
    return task


def delete_task(task_id, user):
    task = repos.get_task_by_id(task_id)
    if not task or task.created_by != user:
        return None
    repos.delete_task(task)
    return task
