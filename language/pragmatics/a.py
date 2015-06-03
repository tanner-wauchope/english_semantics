import re

from language.pragmatics.nouns import Group, Noun


def new_noun(name, hypernym=Noun):
    class NewNoun(hypernym):
        pass
    NewNoun.__name__ = name
    return NewNoun


class IndefiniteArticle:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        if item in self.scope:
            noun = self.scope[item].noun
            self.scope[item].instances.append(noun())
            return noun.group
        elif re.match(r"_[A-Z][a-z]+_$", item):
            noun = new_noun(item[1:-1])
            self.scope[item[1:-1]] = noun.group
            return noun.group
        raise NameError(item)
