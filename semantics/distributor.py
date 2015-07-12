from plain_english.semantics import word_classes


class Distributor:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        noun = self.scope['nouns'][item]
        return word_classes.NounPhrase(
            scope=self.scope,
            kind=noun.kind,
            members=list(noun.members),
        )
