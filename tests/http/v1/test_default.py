# coding=utf-8


def test_ping(client):
    url = '/v1/ping'
    res = client.get(url)
    assert res.status_code == 204
