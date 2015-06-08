from plain_english.pragmatics import nouns


class DefiniteArticle:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        group = self.scope[item]
        result = nouns.Group(self.scope, group.noun)
        result.members = list(group.members)
        result.start = -1
        return result
