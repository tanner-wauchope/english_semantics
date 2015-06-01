import collections

from plain_english.language.pragmatics.verbs import Clause
from plain_english.language.pragmatics.determiners import stack

class Set:
    def __init__(self, noun, instances=None, slice=(None, None)):
        self.noun = noun
        self.instances = instances or collections.OrderedDict()
        self.slice = slice

    def __getattr__(self, item):
        instances = self.instances.values()[self.slice[0]:self.slice[1]]
        return Clause(instances, self.noun.prototype[item])

    def __call__(self, clause):
        for key, instance in self.instances:
            if clause.verb.query(stack, clause, instance):
                self.instances.pop(key, None)
