from . import Verb
from plain_english.pragmatics.nouns import new_subclass


class FaultyAssignment(Exception):
    pass


def copula(self, subject, complement):
    """
    When a verb is used as a key into the predicate dictionary,
    the result is a primitives (set, number, string, etc)
    """
    if not subject.members and not complement.members:
        subject.noun = new_subclass(subject.noun.__name__, complement.noun)
    elif subject.members and not complement.members:
        for instance in subject.instances:
            assert isinstance(instance, complement.noun)
    elif not subject.members and issubclass(complement.noun, subject.noun):
        subject.members = subject.members
    raise FaultyAssignment((subject, complement))

is_ = Verb('is_', copula)






























class Relationship:
    """
    For some sentences, the time the sentence is spoken does not matter.
    These sentences can be repeated or shuffled without a change of meaning.
    These sentences require a subject, because they are not imperative.
    Verbs in these sentences are _stative_.
    """
    relationships_by_subject = {}
    relationships_by_verb = {}
    relationships_by_complement = {}

    def __init__(self, subject, verb, complement=None):
        self.subject = subject
        self.verb = verb
        self.complement = complement

    def __eq__(self, other):
        return (
            self.subject == other.subject and
            self.verb == other.verb and
            self.complement == other.complement
        )

    @classmethod
    def create(cls, subject, verb, complement):
        relationship = cls(subject, verb, complement)
        if subject not in cls.relationships_by_subject:
            cls.relationships_by_subject[subject] = set()
        cls.relationships_by_subject[subject].add(relationship)
        if verb not in cls.relationships_by_verb:
            cls.relationships_by_verb[verb] = set()
        cls.relationships_by_verb[verb].add(relationship)
        if complement not in cls.relationships_by_complement:
            cls.relationships_by_complement[complement] = set()
        cls.relationships_by_complement[complement].add(relationship)
        return relationship

    @classmethod
    def direct_filter(cls, goal):
        result = []
        for relationship in cls.relationships_by_verb[goal.verb]:
            if relationship == goal:
                result.append(relationship)
        return result

    @classmethod
    def transitive_filter(cls, subject, stative_verb, complement):
        checked = set()
        unchecked = cls.direct_filter(subject, stative_verb)
        while unchecked:
            guess = unchecked.pop(0)
            if guess.complement == complement:
                return True
            checked.add(guess)
            candidates = cls.direct_filter(guess.complement, stative_verb)
            for candidate in candidates:
                if candidate not in checked:
                    unchecked.append(candidate)

    @classmethod
    def asymmetric_filter(cls, subject, stative_verb, complement):
        if stative_verb.transitive:
            return cls.transitive_filter(subject, stative_verb, complement)
        else:
            return cls.direct_filter(subject, stative_verb, complement)

    @classmethod
    def symmetric_filter(cls, subject, stative_verb, complement):
        forward = cls.asymmetric_filter(subject, stative_verb, complement)
        backward = cls.asymmetric_filter(complement, stative_verb, subject)
        return forward.union(backward)

    @classmethod
    def filter(cls, subject, stative_verb, complement):
        if stative_verb.commutative:
            return cls.symmetric_filter(subject, stative_verb, complement)
        else:
            return cls.asymmetric_filter(subject, stative_verb, complement)
