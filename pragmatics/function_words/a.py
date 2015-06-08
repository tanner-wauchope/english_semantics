import re

from plain_english.pragmatics.content_words import entity
from plain_english.pragmatics import nouns


class IndefiniteArticle:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        if item in self.scope:
            noun = self.scope[item].noun
            self.scope[item].members.append(noun())
            return nouns.Group(self.scope, noun)
        elif re.match(r"_[A-Z][a-z]+_$", item):
            noun = entity.Entity.new_subclass(item[1:-1])
            self.scope[item[1:-1]] = nouns.Group(self.scope, noun=noun)
            return nouns.Group(self.scope, noun)
        raise NameError(item)
