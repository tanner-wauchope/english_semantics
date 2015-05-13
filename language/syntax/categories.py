from .word import Word


class Clitic(Word):
    """ The word class for possessive suffixes like "'" and "'s". """
    KEYWORDS = {"'", "'s"}
    SPECIFIES = {'Noun'}
    SPECIFIED_BY = {'Noun'}


class Complementizer(Word):
    """ The word class for the relative pronoun "that". """
    KEYWORDS = {'that'}
    COMPLEMENTED_BY = {'Verb'}
    COMPLEMENTS = {'Noun'}


class ConjunctiveAdverb(Word):
    """ The word class for words that stand in for subordinate clauses. """
    KEYWORDS = {'otherwise'}
    SPECIFIED_BY = {'Verb'}


class Determiner(Word):
    """ The word class for articles and quantifiers. """
    KEYWORDS = {'a', 'an', 'any', 'the', 'each'}
    SPECIFIES = {'Noun'}


class Noun(Word):
    """ Open class for capitalized, alphabetic, multi-character lexemes. """
    KEYWORDS = {'it', 'number', 'quote'}
    PATTERN = r"'?[A-Z][a-z]+'?"
    SPECIFIES = {'Verb'}
    COMPLEMENTS = {'Verb'}


class Number(Word):
    """
    The class of spelled numbers and floating-point numbers.
    The regular expression is from Python's documentation:
        https://docs.python.org/3/library/re.html#simulating-scanf
    """
    KEYWORDS = {
        'zero', 'one', 'two', 'three', 'four',
        'five', 'six', 'seven', 'eight', 'nine',
    }
    PATTERN = r"[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?"
    COMPLEMENTS = {'Verb', 'Noun'}


class Possessive(Word):
    """ The class of inherently possessive words. """
    KEYWORDS = {'its', 'their'}
    SPECIFIES = {'Noun'}


class Preposition(Word):
    """ The class of arithmetic operators and other prepositions. """
    KEYWORDS = {'plus', 'minus', 'times', 'over', 'of'}
    COMPLEMENTED_BY = {'Noun', 'Number', 'Variable'}
    COMPLEMENTS = {'Noun', 'Number', 'Variable'}


class Quote(Word):
    """
    The class for embedded quotations.
    The regular expression is from http://stackoverflow.com/questions/249791
    """
    PATTERN = r'"(?:[^"\\]|\\.)*"'
    COMPLEMENTS = {'Noun', 'Verb'}


class Subordinator(Word):
    """ The class of words that begin a subordinate clause. """
    KEYWORDS = {'if', 'while'}
    COMPLEMENTED_BY = {'Verb'}
    SPECIFIED_BY = {'Verb'}


class Variable(Word):
    """ The class of words that represent algebraic variables. """
    PATTERN = r"[A-Z]"
    SPECIFIES = {'Verb'}
    COMPLEMENTS = {'Noun', 'Verb'}


class Verb(Word):
    """ Open class for lowercase, alphabetic, multi-character lexemes. """
    KEYWORDS = {'is', 'has'}
    PATTERN = r"'?[a-z][a-z]+'?"
    COMPLEMENTS = {'Noun'}


# This replace the names in production rules with their values.
# This is needed in Python because of the lack of forward declaration.
for cls in Word.__subclasses__():
    cls.COMPLEMENTED_BY = {eval(name) for name in cls.COMPLEMENTED_BY}
    cls.SPECIFIES = {eval(name) for name in cls.SPECIFIES}
    cls.COMPLEMENTS = {eval(name) for name in cls.COMPLEMENTS}
    cls.SPECIFIED_BY = {eval(name) for name in cls.SPECIFIED_BY}
