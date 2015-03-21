from . import Noun, WorkSet
from syntax.nouns.countable_nouns import CountableNoun

class Query:
    pass


class UncountableNoun(Noun):
    SPECIFIES_TYPES = [CountableNoun]


class PossessiveNoun(UncountableNoun):
    pass


class Quantifier(UncountableNoun):
    pass

Quantifier('all', WorkSet(definite=False))

class String(UncountableNoun):
    pass


class Variable(UncountableNoun):
    pass

