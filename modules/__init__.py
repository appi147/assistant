"""
Modules are handled here
Also, NLP is done here
"""
import json
from forbesqotd import qotd
from basic import user


class Bot():
    """
    This is core of Assistant
    """
    def __init__(self):
        self.actions = (
            "quote",
        )

    def nlp_handler(self, entities, s_id):
        """NLP is done here"""
        responses = []
        for entity in entities:
            if entity == 'greetings' and entities['greetings'][0]['confidence'] >= 0.8:
                responses.append('Hi ' + user(s_id))

        return responses

    def text_handler(self, text):
        """Processes commands"""
        commands = self._find(text)
        responses = []
        for command in commands:
            resp = (getattr(self, command)(text))
            for response in resp:
                responses.append(response)
        return responses

    def _find(self, message):
        """Finds commands"""
        command = []

        words = message.split()
        words_remaining = message.split()

        for word in words:
            words_remaining.remove(word)
            for action in self.actions:
                if word == action:
                    command.append(word)

        return command

    def handler(self, text, entities, s_id):
        """Proceeses and generates replies"""
        resp = []
        responses = self.nlp_handler(entities, s_id)
        for response in responses:
            resp.append(response)
        responses = self.text_handler(text)
        for response in responses:
            resp.append(response)
        return resp

###############################################################################
# Features to be added after this line in alphabetical order
    def quote(self, text=None):
        """Returns a quote"""
        app = qotd.forbes()
        resp = []
        quote = app.get_quote()
        author = app.get_by()
        resp.append(quote)
        resp.append('By ' + author)
        return resp
