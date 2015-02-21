
from . import PartOfSpeech
import sentence_parts

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
            return Singular(self.base)

    def plural(self):
        if self.countable:
            return Plural(pluralize(self.base))

    def uncountable(self):
        if not self.countable:
            return self.Uncountable(self.base)

class Singular(Noun):
    """
    The singular form of a countable noun.
    """
    pass

class Plural(Noun):
    """
    The plural form of a countable noun.
    """
    pass

class Uncountable(Noun):
    """
    A primitives or attributive noun.
    """
    def combine(self, rest):
        next = rest[0]
        if isinstance(next, PluralNoun):
            return sentence_parts.PluralNounPhrase(self, next)
