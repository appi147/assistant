"""
Modules are handled here
Also, NLP is done here
"""
import json
from forbesqotd import qotd
from basic import user
from . import movie, cric


class Bot():
    """
    This is core of Assistant
    """
    def __init__(self):
        self.actions = (
            "cricket",
            "movie",
            "quote",
        )

    def nlp_handler(self, entities, s_id):
        """NLP is done here"""
        responses = []
        for entity in entities:
            if entity == 'greetings' and entities['greetings'][0]['confidence'] >= 0.65:
                responses.append('Hi ' + user(s_id))

        return responses

    def text_handler(self, text):
        """Processes commands"""
        commands = self._find(text)
        responses = []
        for command in commands:
            resp = (getattr(self, command)(text.replace(command, '')))
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
        responses = self.text_handler(text.lower())
        for response in responses:
            resp.append(response)
        return resp

###############################################################################
# Features to be added after this line in alphabetical order
    def cricket(self, text=None):
        """Cricket scores"""
        resp = []
        options = ['live', 'preview', 'result']
        for option in options:
            if option in text:
                resp.extend(getattr(cric, option)())
        return resp

    def movie(self, text=None):
        """Movie-IMDb"""
        return ['Movie feature is currently down']
        resp = []
        options = ["cast", "director", "plot", "producer", "rating", "year"]
        movieName = text
        for option in options:
            movieName = movieName.replace(option, '')
        for i in range(len(options)):
            movieName.replace('  ', ' ')
        for option in options:
            if option in text:
                resp.append(option + ': ' + str(getattr(movie, option)(movieName)))
        return resp

    def quote(self, text=None):
        """Returns a quote"""
        app = qotd.forbes()
        resp = []
        quote = app.get_quote()
        author = app.get_by()
        resp.append(quote)
        resp.append('By ' + author)
        return resp
