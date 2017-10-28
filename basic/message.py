"""
Various types of message templates are stored here
"""
import os
import json
import requests
from . import log


def text(recipient_id, message_text):
    """This is test message"""
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages",
                         params=params, headers=headers, data=data)
    if resp.status_code != 200:
        log(resp.status_code)
        log(resp.text)
