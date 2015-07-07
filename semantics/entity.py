from plain_english.semantics.nouns import Noun
from plain_english.semantics.verbs import Verb


class ContradictionError(Exception):
    pass


class Entity(Noun):
    pass


class Copula(Verb):
    def run(self, subject, complement):
        if issubclass(complement.noun, subject.noun):
            sets = [sender.values for sender in complement.members]
            package = set.union(*sets)
            for receiver in subject.members:
                if receiver.value and receiver.value != package:
                    raise ContradictionError((receiver.value, package))
                receiver.values = package
        raise TypeError((subject, complement))

    def define(self, subject, complement, support_sentences):
        name = subject.noun.__name__
        prototype = subject.noun.prototype
        noun = complement.noun.new_subclass(name, prototype)
        subject.scope[subject.noun.__name__] = noun

Noun.prototype['is_'] = Copula('is_')


class Possessive(Verb):
    def run(self, subject, complement):
        for member in subject.members:
            current = member.possessions.get(complement.noun)
            if current and current != complement:
                raise ContradictionError
            member.possessions[complement.noun] = complement


Noun.prototype['has_'] = Possessive('has_')
