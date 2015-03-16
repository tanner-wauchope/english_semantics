import time

class Event:
    """
    For some sentences, the time that the sentence is spoken matters.
    Repeating or shuffling these sentences results in a different meaning.
    """
    pending = []

    def __init__(self, verb, complement=None, execute_after=None):
        self.verb = verb
        self.complement = complement
        self.execute_after = execute_after or time.time()

    @classmethod
    def process_events(cls):
        now = time.time()
        for event in cls.pending:
            if event.end and event.end < now:
                event.verb.execute_side_effect(event)
                cls.pending.remove(event)

    @classmethod
    def create(cls, verb, complement=None, execute_after=None):
        event = Event(verb, complement, execute_after)
        cls.pending.append(event)
        return event

class Relationship:
    """
    For some sentences, the time the sentence is spoken does not matter.
    These sentences can be repeated or shuffled without a change of meaning.
    """
    relationships = {}

    def __init__(self, subject, complement):
        self.subject = subject
        self.complement = complement

    def __eq__(self, other):
        return (
            self.subject == other.subject and
            self.complement == other.complement
        )

    @classmethod
    def create(cls, subject, stative_verb, complement):
        relationship = cls(subject, complement)
        if stative_verb not in cls.relationships:
            cls.relationships[stative_verb] = set()
        cls.relationships[stative_verb].add(relationship)
        return relationship

    @classmethod
    def direct_filter(cls, subject, stative_verb, complement):
        result = set()
        goal = Relationship(subject, complement)
        for relationship in cls.relationships[stative_verb]:
            if relationship == goal:
                result.add(relationship)
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


