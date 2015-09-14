import re

from plain_english.semantics import predicate


class An:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        """
        :param item: the name of a noun or a name wrapped in '_'
        :return: a noun with the entity class specified by 'item'
                 if 'item' was wrapped in '_',
                    instantiate a noun with no Entity class
        """
        if item in self.scope['singular']:
            phrase = self.scope['singular'][item]
            return predicate.OrderedSet(item, kind=phrase.kind, scope=self.scope)
        elif re.match(r"_[A-Z][a-z]+_$", item):
            singular = item[1:-1]
            phrase = predicate.OrderedSet(
                singular,
                number=None,
                scope=self.scope
            )
            self.scope[phrase.plural] = phrase
            self.scope['singular'][singular] = phrase
            return predicate.OrderedSet(singular, scope=self.scope)
        raise NameError(item)


class The:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        if item in self.scope['singular']:
            phrase = self.scope['singular'][item]
            return predicate.OrderedSet(
                item,
                plural=phrase.plural,
                kind=phrase.kind,
                number=1,
                members=list(phrase.members),
                scope=self.scope,
            )
        elif item in self.scope:
            phrase = self.scope[item]
            return predicate.OrderedSet(
                item,
                plural=phrase.plural,
                kind=phrase.kind,
                number=None,
                members=list(phrase.members),
                scope=self.scope,
            )
        raise NameError(item)

