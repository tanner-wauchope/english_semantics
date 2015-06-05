from .nouns import Group


class Distributor:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        return Group(self.scope[item])
