from plain_english.pragmatics.nouns import Noun
from plain_english.pragmatics.verbs import Verb


class FaultyAssignment(Exception):
    pass


class Entity(Noun):
    prototype = {}


def copula(self, subject, complement):
    """
    When a verb is used as a key into the predicate dictionary,
    the result is a primitives (set, number, string, etc)
    """
    if not subject.members and not complement.members:
        name = subject.noun.__name__
        prototype = subject.noun.prototype
        subject.noun = complement.noun.new_subclass(name, prototype)
    elif subject.members and not complement.members:
        for instance in subject.instances:
            assert isinstance(instance, complement.noun)
    elif not subject.members and issubclass(complement.noun, subject.noun):
        subject.members = subject.members
    raise FaultyAssignment((subject, complement))

Entity.prototype['is_'] = Verb('is_', copula)


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
