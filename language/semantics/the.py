import collections

from .all_ import all_
from .a import a
from.nouns import Query

class DefiniteArticle:
    def __init__(self):
        self.instances = collections.defaultdict(set)

    def __getattr__(self, item):
        if item in all_.nouns:
            declension = all_.nouns[item]
            return Query(declension, self.instances[declension])
        elif item in a.nouns:
            declension = a.nouns[item]
            return Query(declension, self.instances[declension])
        raise NameError(item)

the = DefiniteArticle()
