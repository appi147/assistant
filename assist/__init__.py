import json


def handler(entities, text):
    response = []
    for entity in entities:
        if entity == 'greetings' and entities['greetings'][0]['confidence'] >= 0.8:
            response.append('greetings')
    return response
