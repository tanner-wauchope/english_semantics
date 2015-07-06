import re

from plain_english.pragmatics import entity
from plain_english.semantics import nouns


class IndefiniteArticle:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        if item in self.scope['nouns']:
            noun = self.scope[item].noun
            self.scope['nouns'][item].members.append(noun())
            return nouns.Group(self.scope, noun)
        elif re.match(r"_[A-Z][a-z]+_$", item):
            name = item[1:-1]
            noun = entity.Entity.new_subclass(name)
            self.scope['nouns'][name] = nouns.Group(self.scope, noun=noun)
            return nouns.Group(self.scope, noun)
        raise NameError(item)
