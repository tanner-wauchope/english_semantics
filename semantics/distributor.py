from plain_english.semantics import open_classes


class Distributor:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        noun = self.scope['nouns'][item]
        result = open_classes.Noun(self.scope, noun.kind)
        result.members = list(noun.members)
        return result
