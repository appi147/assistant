import sys
import os
import json


def handler(entities, text):
    response = []
    for entity in entities:
        if entity == 'greetings' and entity['confidence'] >= 0.8:
            response.append('greetings')
    return response

def log(message):
    print(str(message))
    sys.stdout.flush()

def user(sender):
    r = requests.get('https://graph.facebook.com/v2.6/' + str(sender), params={
                'fields': 'first_name',
                'access_token': os.environ["PAGE_ACCESS_TOKEN"]
            })
    user_data = r.json()
    return user_data['first_name']