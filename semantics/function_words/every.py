from plain_english.semantics import nouns


class Distributor:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        group = self.scope[item]
        result = nouns.Group(self.scope, group.noun)
        result.members = list(group.members)
        return result
