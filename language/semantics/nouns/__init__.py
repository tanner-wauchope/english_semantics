from plain_english.language.semantics.verbs import Clause


class Noun:
    def __init__(self):
        self.referenced_by = {}
        self.singular = Declension(self)
        self.plural = Declension(self)


class Declension:
    def __init__(self, noun):
        self.noun = noun
        self.references = {}


class Set:
    def __init__(self, declension, instances, start_index=None):
        self.declension = declension
        self.instances = instances
        self.start_index = start_index

    def __getattr__(self, item):
        instances = self.instances[self.start_index:]
        if item in self.declension.references:
            return Clause(instances, self.declension.references[item])
        raise NameError(item)

    def __call__(self, clause):
        self.instances = [i for i in self.instances if clause.complements(i)]
