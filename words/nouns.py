
from . import PartOfSpeech
import constituency

def pluralize(base):
    if base.endswith('s'):
        return base + 'es'
    elif base.endswith('y'):
        return base[:-1] + 'ies'
    return base + 's'

class Noun(PartOfSpeech):
    def __init__(self, base, countable=True):
        self.base = base
        self.countable = countable

    def singular(self):
        if self.countable:
            return SingularNoun(self.base)

    def plural(self):
        if self.countable:
            return PluralNoun(pluralize(self.base))

    def uncountable(self):
        if not self.countable:
            return self.UncountableNoun(self.base)

class SingularNoun(Noun):
    """
    The singular form of a countable noun.
    """
    pass

class PluralNoun(Noun):
    """
    The plural form of a countable noun.
    """
    pass

class UncountableNoun(Noun):
    """
    A primitives or attributive noun.
    """
    def combine(self, rest):
        next = rest[0]
        if isinstance(next, PluralNoun):
            return constituency.PluralNounPhrase(self, next)
