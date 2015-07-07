from plain_english.semantics import nouns


class DefiniteArticle:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        context = self.scope['nouns'][item]
        result = nouns.Group(self.scope, context.noun)
        result.members = list(context.members)
        result.start = -1
        return result
