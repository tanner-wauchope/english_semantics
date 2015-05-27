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