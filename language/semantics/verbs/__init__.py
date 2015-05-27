from language.semantics.the import the


class ContradictionError(Exception):
    pass


class SubjectVerbMismatch(Exception):
    pass


class VerbComplementMismatch(Exception):
    pass


class Verb:
    def __init__(self, procedure):
        self.procedure = procedure
        self.singular = Conjugation(self)
        self.plural = Conjugation(self)


class Conjugation:
    def __init__(self, verb):
        self.references = {}
        self.verb = verb

    def __call__(self, complement):
        if complement.declension in self.references:
            return Clause(conjugation=self, complement=complement)
        raise NameError

    def run(self, subject, complement, supporting_sentences):
        if self is self.verb.singular:
            self.verb.procedure(subject, complement, supporting_sentences)
        else:
            for instance in subject:
                self.verb.procedure(instance, complement, supporting_sentences)


class Clause:
    def __init__(self, subject=None, conjugation=None, complement=None):
        self.subject = subject
        self.conjugation = conjugation
        self.complement = complement

    def __call__(self, *complements):
        if self.is_incomplete(complements):
            self.complement = complements[0]
        else:
            self.conjugation.run(self.subject, self.complement, complements)
            the.queries = {}

    def is_incomplete(self, complements):
        return (
            not self.complement and
            len(complements) is 1 and
            isinstance(complements[0], Instance) and
            complements[0] in self.conjugation.references and
            self.conjugation.accepts(self.subject, complements[0])
        )

    def complements(self, instance):
        if self.subject:
            return self.conjugation.accepts(self.subject, instance)
        elif self.complement:
            return self.conjugation.accepts(instance, self.complement)
        return False
