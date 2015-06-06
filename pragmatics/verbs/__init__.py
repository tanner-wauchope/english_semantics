import types

from plain_english.pragmatics import new_scope


class Verb:
    def __init__(self, name, procedure=None):
        self.name = name
        self.complements = {}
        if procedure:
            self.procedure = types.MethodType(procedure, self)
        else:
            self.procedure = self.default_procedure

    def default_procedure(self, topic_sentence, support_sentences):
        topic_sentence.subject.noun.prototype[self.name] = self
        self.complements[topic_sentence.complement.noun] = set()
        def new_procedure(subject, complement):
            new_scope(locals())
            locals()[topic_sentence.subject.noun.name] = subject
            locals()[topic_sentence.complement.noun.name] = complement
            exec(support_sentences)
        self.procedure = new_procedure


class Clause:
    def __init__(self, subject=None, verb=None, complement=None):
        self.subject = subject
        self.verb = verb
        self.complement = complement

    def __call__(self, *complements):
        if isinstance(complements[0], Clause):
            self.subject.predicates[self.verb].complements[self.complement] = \
                self.verb.procedure(self, complements)
        else:
            self.complement = complements[0]
            return self

