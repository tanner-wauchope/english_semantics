from plain_english.semantics import verbs


class Complementizer:
    def __getattr__(self, item):
        return verbs.Clause(verb=item)
