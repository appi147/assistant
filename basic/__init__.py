import os
import requests
import json
import sys


def user(sender):
    r = requests.get('https://graph.facebook.com/v2.6/' + str(sender), params={
                'fields': 'first_name',
                'access_token': os.environ["PAGE_ACCESS_TOKEN"]
            })
    user_data = r.json()
    return user_data['first_name']


def log(message):
    print(str(message))
    sys.stdout.flush()