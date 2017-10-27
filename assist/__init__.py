import json


def handler(entities, text):
    entities = entities.json()
    response = []
    for entity in entities:
        if entity == 'greetings' and entity['confidence'] >= 0.8:
            response.append('greetings')
    return response
