
from . import PartOfSpeech

class Determiner(PartOfSpeech):
    def combine(self, rest):
        next = rest[0]
        if isinstance(next, UncountableNoun):
            return Specifier(self, next)
        return Specifier(self)