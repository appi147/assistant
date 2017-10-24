def handler(entities, text):
    for entity in entities:
        log(entity)

def log(message):
    print(str(message))
    sys.stdout.flush()