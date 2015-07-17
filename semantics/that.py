from plain_english.semantics import word_classes


class That:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        if item in ('a', 'an', 'the', 'every'):
            return self.scope[item]
        return word_classes.VerbPhrase(item)
