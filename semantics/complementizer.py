from plain_english.semantics import open_classes


class Complementizer:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        if item in ('a', 'an', 'the', 'every'):
            return self.scope[item]
        return open_classes.Verb(verb=item)
