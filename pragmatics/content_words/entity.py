from plain_english.pragmatics.nouns import Noun
from plain_english.pragmatics.verbs import Verb


class ContradictionError(Exception):
    pass


class TypeError(Exception):
    pass


class Entity(Noun):
    prototype = {}


class Copula(Verb):
    def run(self, subject, complement):
        """ what if the complement is primitive? """
        if issubclass(complement.noun, subject.noun):
            package = [sender.value for sender in complement.members]
            for receiver in subject.members:
                if receiver.value and receiver.value != package:
                    raise ContradictionError((receiver.value, package))
                receiver.values = package
        raise TypeError((subject, complement))

    def define(self, subject, complement, support_sentences):
        name = subject.noun.__name__
        prototype = subject.noun.prototype
        subject.noun = complement.noun.new_subclass(name, prototype)

Entity.prototype['is_'] = Copula('is_')


def possessive(self, subject, complement):
    """
    param complement: a Group or a callable complement-retriever
    When the key used to lookup a value from the prototype
    dictionary is a verb, the result is a set of instances
    or a function
    """
    if not subject.members and not complement.members:
        subject.noun.prototype[self].complements[complement.noun] = complement
    elif subject.members and not complement.members:
        for member in complement.members:
            member.predicates[self].complements[complement.noun] = complement

Entity.prototype['has_'] = Verb('has_', possessive)
