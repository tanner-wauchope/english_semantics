from .determiners import Determiner
from .conjunctions import Conjunction
from .prepositions import Preposition
from .nouns import Noun
from .verbs import Verb


class Container:
    """
    May accept a rightward argument
    If the argument is a modifier, return a container
    If the argument is a predicate, execute side-effects
    """
    pass

class Complement:
    """
    Modifies a work set
    """
    pass

class Specifier:
    """
    Accepts a rightward specifier or container
    If the argument is a specifier, return a specifier
    If the argument is a container, return a container
    """
    pass

class Operator:
    """
    Accepts one rightward container
    Returns a complement
    """
    pass

class Predicate:
    """
    # May accepts 1 rightward complement
    # Returns an event that encapsulates a side-effect
    """
    pass

class Word:
    def __init__(self, spelling, meaning):
        self.spelling = spelling
        self.meaning = meaning

    @property
    def meaning(self):


########

class Noun(PartOfSpeech):
    pass

class CountableNoun(Noun):
    def workset(self, *subtypes, determiner=None):
        result = Workset(self, *subtypes)
        if determiner:
            result.fill(self.determiner.count())
        return result

class UncountableNoun(Noun):
    def combine(self, next):
        if isinstance(next, PluralCountableNoun):
            return PluralNounPhrase(next.workset(self))
        return SingularNounPhrase(self.workset()).combine(next)

class Determiner(PartOfSpeech):
    def combine(self, next):
        if isinstance(next, UncountableNoun):
            return AttributiveSpecifier(self, next)
        elif isinstance(next, CountableNoun):
            return NounPhrase.cast(
                next.workset(self, next)
            )

class Conjunction(PartOfSpeech):
    pass

class Preposition(PartOfSpeech):
    pass

class Verb(PartOfSpeech):
    pass

class Copula(Verb):
    pass

class SingularCopula(Copula):
    pass

class PluralCopula(Copula):
    pass

class LexicalVerb(Verb):
    pass

class SingularLexicalVerb(LexicalVerb):
    pass

class PluralLexicalVerb(LexicalVerb):
    pass