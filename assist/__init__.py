import sys
import os
import json


def handler(entities, text):
    log(entities)
    for entity in entities:
        log(entity)
    log(text)

def log(message):
    print(str(message))
    sys.stdout.flush()