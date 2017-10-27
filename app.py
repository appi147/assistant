import os
import sys
import json
import requests
from flask import Flask, request, render_template
from assist import handler


app = Flask(__name__)


def log(message):
    print(str(message))
    sys.stdout.flush()


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe"and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    # return "Assistant", 200
    return render_template('index.html'), 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):

                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = messaging_event["message"]["text"]
                    nlp = messaging_event["message"]["nlp"]
                    entities = nlp["entities"]
                    execute(sender_id, entities, message_text)

    return "ok", 200

def execute(sender_id, entities, text):
    user(sender_id)
    responses = handler(entities, text)
    for response in responses:
        if response == 'greetings':
            send_text(sender_id, 'Hi' + user(sender_id))
    reply = "Assistant is currently under development"
    send_text(sender_id, reply)


def send_text(recipient_id, message_text):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def user(sender):
    r = requests.get('https://graph.facebook.com/v2.6/' + str(sender), params={
                'fields': 'first_name',
                'access_token': os.environ["PAGE_ACCESS_TOKEN"]
            })
    user_data = r.json()
    return user_data['first_name']

if __name__ == '__main__':
    app.run(debug=True)
