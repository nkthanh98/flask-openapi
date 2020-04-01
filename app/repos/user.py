# coding=utf-8

from app import models


def get_user_by_id(user_id):
    return models.session.query(models.User).get(user_id)


def get_user_by_username(username):
    return models.session.query(
        models.User
    ).filter(
        models.User.username == username
    ).first()


def create_user(fullname, username, password):
    new_user = models.User(
        username=username,
        password=password,
        fullname=fullname
    )
    models.session.add(new_user)
    models.session.commit()
    return new_user


def update_user(user_id_or_user, data):
    if isinstance(user_id_or_user, int):
        user = get_user_by_id(user_id_or_user)
    else:
        user = user_id_or_user
    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    models.session.commit()
    return user
