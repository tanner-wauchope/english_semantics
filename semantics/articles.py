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
            singular = predicate.OrderedSet(name, number=None, scope=self.scope)
            self.scope['nouns'][name] = singular
            plural = self.create_plural(name, singular.kind)
            self.scope['nouns'][plural.name] = plural
            return predicate.OrderedSet(name, scope=self.scope)
        raise NameError(item)

    def create_plural(self, singular, kind):
        """
        :param singular: the singular spelling
        :param kind: the class for the noun
        :return: a plural noun phrase with default spelling
        """
        if singular.endswith('h'):
            plural = singular + 'es'
        elif singular.endswith('s'):
            plural =  singular + 'es'
        elif singular.endswith('o') and singular[-2] not in 'aeiou':
            plural =  singular + 'es'
        elif singular.endswith('y') and singular[-2] not in 'aeiou':
            plural =  singular[:-1] + 'ies'
        else:
            plural =  singular + 's'
        return predicate.OrderedSet(
            plural,
            kind=kind,
            number=0,
            scope=self.scope,
        )


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
