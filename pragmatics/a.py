import re

from .nouns import new_subclass, Group


class IndefiniteArticle:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        if item in self.scope:
            noun = self.scope[item].noun
            self.scope[item].members.append(noun())
            return noun.group
        elif re.match(r"_[A-Z][a-z]+_$", item):
            noun = new_subclass(item[1:-1])
            self.scope[item[1:-1]] = Group(noun=noun)
            return Group(noun=noun)
        raise NameError(item)
