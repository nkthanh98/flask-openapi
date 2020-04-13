# coding=utf-8

import requests
from app.jobs import manager


@manager.task(serializer='json')
def send_message_to_slack_channel(token, channel_id, message):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    body = {
        'channel': channel_id,
    }
    if isinstance(message, str):
        body['text'] = message
    elif isinstance(message, list):
        body['attachments'] = message
    else:
        body['text'] = str(message)
    resp = requests.post(
        url=url,
        json=body,
        headers=headers
    )
    return resp.json()
