from .nouns import Group


class DefiniteArticle:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        return Group(self.scope[item], -1)
