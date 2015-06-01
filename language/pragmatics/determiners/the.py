import collections

from plain_english.language.pragmatics.nouns import Set


class DefiniteArticle:
    def __init__(self, stack):
        self.stack = stack

    def __getattr__(self, item):
        instance_set = self.stack[item]
        instances = collections.OrderedDict(instance_set.instances)
        return Set(instance_set.noun, instances, (None, -1))
