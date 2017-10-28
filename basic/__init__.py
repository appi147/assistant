"""
Basic functions to be used are defined here
"""
import os
import json
import sys
import requests


def user(sender):
    """
    This fetches information about user
    """
    resp = requests.get('https://graph.facebook.com/v2.6/' + str(sender),
                        params={
                            'fields': 'first_name',
                            'access_token': os.environ["PAGE_ACCESS_TOKEN"]
                            })
    user_data = resp.json()
    return user_data['first_name']


def log(message):
    """
    Logs message in Heroku
    """
    print(str(message))
    sys.stdout.flush()
