import re

from plain_english.semantics.primitives import entity
from plain_english.semantics import word_classes


class IndefiniteArticle:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        """
        :param item: the name of a noun or a name wrapped in '_'
        :return: a noun with the entity class specified by 'item'
                 if 'item' was wrapped in '_',
                    instantiate a noun with no Entity class
        """
        if item in self.scope['nouns']:
            kind = self.scope['nouns'][item].kind
            return word_classes.NounPhrase(self.scope, kind)
        elif re.match(r"_[A-Z][a-z]+_$", item):
            context = word_classes.NounPhrase(self.scope, entity.Entity)
            self.scope['nouns'][item[1:-1]] = context
            return word_classes.NounPhrase(self.scope, entity.Entity)
        raise NameError(item)
