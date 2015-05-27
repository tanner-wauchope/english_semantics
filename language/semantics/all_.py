
class UniversalQuantifier:
    def __init__(self):
        self.nouns = {}

    def __getattr__(self, item):
        if item in self.nouns:
            return self.nouns[item]
        raise NameError(item)

all_ = UniversalQuantifier()