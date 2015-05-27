from plain_english.language.semantics.verbs import Clause


class Query:
    def __init__(self, declension, instances):
        self.declension = declension
        self.instances = instances

    def __getattr__(self, item):
        if item in self.declension.references:
            return Clause(self.instances, self.declension.references[item])
        raise NameError(item)

    def __call__(self, clause):
        instances = []
        for instance in self.instances:
            if clause.complements(instance):
                instances.append(instance)
        return instances


class Noun:
    def __init__(self):
        self.referenced_by = {}
        self.singular = Declension(self)
        self.plural = Declension(self)


class Declension:
    def __init__(self, noun):
        self.noun = noun
        self.references = {}
