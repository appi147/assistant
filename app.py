"""
This is the main program which contains
GET and POST methods
"""
import os
from flask import Flask, request, render_template
from modules import Bot
from basic import log, user, message


APP = Flask(__name__)


@APP.route('/', methods=['GET'])
def verify():
    """
    This verifies Tokens and renders webpage
    """
    if request.args.get("hub.mode") == "subscribe"and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return render_template('index.html'), 200


@APP.route('/privacypolicy', methods=['GET'])
def privacy_policy():
    """
    Our privacy policy
    """
    return render_template('privacypolicy.html'), 200


@APP.route('/', methods=['POST'])
def webhook():
    """
    Webhook is set here and message is extracted for processing
    """
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
    """
    Message is processed and reply is generated
    """
    user(sender_id)
    bot = Bot()
    responses = bot.handler(text, entities, sender_id)
    responses.append("Assistant is currently under development")
    log(responses)
    for reply in responses:
        message.text(sender_id, reply)


if __name__ == '__main__':
    APP.run(debug=True)
