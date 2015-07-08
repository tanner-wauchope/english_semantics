import re

from plain_english.semantics import entity
from plain_english.semantics import nouns


class IndefiniteArticle:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        """
        :param item: the name of a noun or a name wrapped in '_'
        :return: an empty Group with the noun specified by 'item'
                 if 'item' was wrapped in '_', instantiate a noun
        """
        if item in self.scope['nouns']:
            noun = self.scope['nouns'][item].noun
            return nouns.Group(self.scope, noun)
        elif re.match(r"_[A-Z][a-z]+_$", item):
            name = item[1:-1]
            noun = type(name, (entity.Entity,), {})
            self.scope['nouns'][name] = nouns.Group(self.scope, noun=noun)
            return nouns.Group(self.scope, noun)
        raise NameError(item)
