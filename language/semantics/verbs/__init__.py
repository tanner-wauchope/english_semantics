from plain_english.language.semantics import the


class Verb:
    def __init__(self, procedure, function):
        self.procedure = procedure
        self.function = function
        self.references = {}

    def __call__(self, complement):
        if complement.noun in self.references:
            return Clause(verb=self, complement=complement)
        raise NameError


class Clause:
    def __init__(self, subject=None, verb=None, complement=None):
        self.subject = subject
        self.verb = verb
        self.complement = complement

    def __call__(self, *complements):
        if complements[0] in self.subject.references:
            self.complement = complements[0]
        else:
            self.verb.procedure(self, complements)
            the.instances = {}

    def complements(self, instance):
        if self.subject:
            return self.verb.function(self.subject, instance)
        elif self.complement:
            return self.verb.function(instance, self.complement)
        return False
