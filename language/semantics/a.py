import re

from .nouns import Noun, Query
from .the import the
from .all_ import all_


class IndefiniteArticle:
    def __init__(self):
        self.nouns = {}

    def __getattr__(self, item):
        if item in self.nouns:
            noun = self.nouns[item]
            instance = noun.references.copy()
            the.instances[noun].add(instance)
            return Query(noun, instance)
        elif re.match(r"_[A-Z][a-z]+_$", item):
            noun = Noun()
            name = item[1:-1]
            self.nouns[name] = noun
            all_.nouns[regular_plural(name)] = noun
            all_.nouns[semi_regular_plural(name)] = noun
            return noun
        raise NameError(item)

a = an = IndefiniteArticle()


def regular_plural(singular):
    if singular.endswith('h'):
        return singular + 'es'
    elif singular.endswith('s'):
        return singular + 'es'
    elif singular.endswith('o') and singular[-2] not in 'aeiou':
        return singular + 'es'
    elif singular.endswith('y') and singular[-2] not in 'aeiou':
        return singular[:-1] + 'ies'
    return singular + 's'


def semi_regular_plural(singular):
    if singular.endswith('ma'):
        return singular + 'ta'
    elif singular.endswith('a'):
        return singular + 'e'
    elif singular.endswith('fe'):
        return singular[:-2] + 'ves'
    elif singular.endswith('f'):
        return singular[:-1] + 'ves'
    elif singular.endswith('um'):
        return singular[:-2] + 'a'
    elif singular.endswith('on'):
        return singular[:-2] + 'a'
    elif singular.endswith('o'):
        return singular + 'o'
    elif singular.endswith('is'):
        return singular[:-2] + 'es'
    elif singular.endswith('us'):
        return singular[:-2] + 'i'
    elif singular.endswith('x'):
        return singular[:-1] + 'ces'
