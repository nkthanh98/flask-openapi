# coding=utf-8


def test_ping(app):
    url = '/v1/ping'
    res = app.test_client().get(url)
    assert res.status_code == 204
