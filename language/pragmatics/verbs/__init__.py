from plain_english.language.pragmatics.determiners import stack


class Verb:
    def __init__(self, procedure, query, complement):
        self.procedure = procedure
        self.query = query
        self.complement = complement

    def __call__(self, complement):
        if complement.noun is self.complement:
            return Clause(verb=self, complement=complement)
        raise NameError


class Clause:
    def __init__(self, subject=None, verb=None, complement=None):
        self.subject = subject
        self.verb = verb
        self.complement = complement

    def __call__(self, *complements):
        if complements[0].noun in self.verb.references:
            self.complement = complements[0]
            return self
        else:
            stack.append({})
            self.verb.procedure(stack, self, complements)
            stack.pop()
