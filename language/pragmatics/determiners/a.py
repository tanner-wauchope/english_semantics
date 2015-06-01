import collections
import re

from language.pragmatics.nouns import Set


def new_noun():
    class NewNoun:
        prototype = {}

        def __init__(self):
            self.state = self.prototype.copy()

    return NewNoun


class IndefiniteArticle:
    def __init__(self, stack):
        self.stack = stack

    def __getattr__(self, item):
        if item in self.stack:
            noun = self.stack[item].noun
            instance = noun()
            self.stack[-1][item].instances[id(instance)] = instance
            return Set(noun, collections.OrderedDict({id(instance): instance}))
        elif re.match(r"_[A-Z][a-z]+_$", item):
            noun = new_noun()
            self.stack[item[1:-1]] = Set(noun)
            return Set(noun)
        raise NameError(item)
