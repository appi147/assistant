"""
Modules are handled here
Also, NLP is done here
"""
import json


def handler(entities):
    """NLP is done here"""
    response = []
    for entity in entities:
        if entity == 'greetings' and entities['greetings'][0]['confidence'] >= 0.8:
            response.append('greetings')
    return response


def text_handler(text):
    """Processes commands"""
    pass
