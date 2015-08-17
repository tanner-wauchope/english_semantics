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
        if item in self.scope['nouns']:
            kind = self.scope['nouns'][item].kind
            return predicate.OrderedSet(item, kind=kind, scope=self.scope)
        elif re.match(r"_[A-Z][a-z]+_$", item):
            name = item[1:-1]
            context = predicate.OrderedSet(name, number=None, scope=self.scope)
            self.scope['nouns'][name] = context
            return predicate.OrderedSet(name, scope=self.scope)
        raise NameError(item)


class The:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        noun = self.scope['nouns'][item]
        return predicate.OrderedSet(
            item,
            kind=noun.kind,
            number=1,
            members=list(noun.members),
            scope=self.scope,
        )


class All:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        noun = self.scope['nouns'][item]
        return predicate.OrderedSet(
            item,
            kind=noun.kind,
            number=0,
            members=list(noun.members),
            scope=self.scope,
        )
