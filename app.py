import os
from flask import Flask, request, render_template
from assist import handler
from basic import log, user, message


APP = Flask(__name__)



@APP.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe"and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    # return "Assistant", 200
    return render_template('index.html'), 200


@APP.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):

                    sender_id = messaging_event["sender"]["id"]
                    # recipient_id = messaging_event["recipient"]["id"]
                    message_text = messaging_event["message"]["text"]
                    nlp = messaging_event["message"]["nlp"]
                    entities = nlp["entities"]
                    log(entities)
                    execute(sender_id, entities, message_text)

    return "ok", 200


def execute(sender_id, entities, text):
    user(sender_id)
    responses = handler(entities, text)
    for response in responses:
        if response == 'greetings':
            reply = 'Hi' + user(sender_id)
            log(reply)
            message.text(sender_id, reply)
    reply = "Assistant is currently under development"
    message.text(sender_id, reply)


if __name__ == '__main__':
    APP.run(debug=True)
