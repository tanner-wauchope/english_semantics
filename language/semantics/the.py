import collections

from.nouns import Set


class DefiniteArticle:
    def __init__(self, all_):
        self.all_ = all_
        self.instances = collections.defaultdict(Set)

    def __getattr__(self, item):
        if item in self.all_.nouns:
            declension = self.all_.nouns[item]
            return Set(declension, self.instances[declension], -1)
        elif item in self.instances:
            declension = self.declensions[item]
            return Set(declension, self.instances[declension], -1)
        raise NameError(item)
