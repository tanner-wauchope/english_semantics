import re

from .nouns import Noun, Set

class IndefiniteArticle:
    def __init__(self, the, all_):
        self.the = the
        self.all_ = all_
        self.nouns = {}

    def __getattr__(self, item):
        if item in self.nouns:
            noun = self.nouns[item]
            instance = noun.singular.references.copy()
            self.the.instances[item].add(instance)
            return Set(noun, instance)
        elif re.match(r"_[A-Z][a-z]+_$", item):
            noun = Noun()
            name = item[1:-1]
            self.nouns[name] = noun
            self.all_.nouns[pluralize(name)] = noun
            return noun
        raise NameError(item)


def pluralize(singular):
    if singular.endswith('h'):
        return singular + 'es'
    elif singular.endswith('s'):
        return singular + 'es'
    elif singular.endswith('o') and singular[-2] not in 'aeiou':
        return singular + 'es'
    elif singular.endswith('y') and singular[-2] not in 'aeiou':
        return singular[:-1] + 'ies'
    return singular + 's'
