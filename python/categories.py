import keyword

from .word import Word


def python(word, prefix='', suffix=''):
    if word is None:
        return ''
    else:
        return prefix + word.python() + suffix


class Clitic(Word):
    """ The word class for possessive suffixes like "'" and "'s". """
    KEYWORDS = {"'", "'s"}
    SPECIFIES = {'Noun'}
    SPECIFIED_BY = {'Noun'}

    def python(self):
        return '{specifier}.'.format(specifier=self.specifier.python())


class Complementizer(Word):
    """ The word class for the relative pronoun "that". """
    KEYWORDS = {'that'}
    COMPLEMENTED_BY = {'Verb'}
    COMPLEMENTS = {'Noun'}

    def python(self):
        return ''


class And(Word):
    """ The word that tuples noun phrases. """
    KEYWORDS = {'and'}
    COMPLEMENTED_BY = {'Noun', 'Verb'} # type check to ensure consistency
    SPECIFIED_BY = {'Noun', 'Verb'}

    def python(self):
        return '{0} & {1}'.format(
            self.specifier.python(),
            self.complement.python(),
        )


class Or(Word):
    """ Indicates a statement is a backup to the previous statement. """
    KEYWORDS = {'or'}
    COMPLEMENTED_BY = {'Noun', 'Verb'} # type check to ensure consistency
    SPECIFIED_BY = {'Noun', 'Verb'}

    def python(self):
        return 'else:'


class Determiner(Word):
    """ The word class for articles and quantifiers. """
    KEYWORDS = {'a', 'an', 'the'}
    SPECIFIES = {'Noun'}

    def python(self):
        return ''


class Noun(Word):
    """ Open class for capitalized, alphabetic, multi-character lexemes. """
    KEYWORDS = {'it', 'number', 'numbers', 'quote', 'quotes'}
    PATTERN = r"[A-Za-z]+[0-9]*"
    SPECIFIES = {'Verb'}
    COMPLEMENTS = {'Verb'}

    def python(self):
        return '{0}{1}{2}'.format(
            python(self.specifier),
            self.head.lower(),
            python(self.complement),
        )


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

    def python(self):
        return self.head


class Preposition(Word):
    """ The class of prepositions. """
    KEYWORDS = {'of'}
    COMPLEMENTED_BY = {'Noun', 'Number'}
    COMPLEMENTS = {'Noun', 'Number'}

    def python(self):
        return '({noun_phrase})'.format(noun_phrase=self.complement.python())


class Quote(Word):
    """
    The class for embedded quotations.
    The regular expression is from http://stackoverflow.com/questions/249791
    """
    PATTERN = r'"(?:[^"\\]|\\.)*"'
    COMPLEMENTS = {'Noun', 'Verb'}

    def python(self):
        return self.head


class Subordinator(Word):
    """ The class of words that begin a subordinate clause. """
    KEYWORDS = {'if'}
    COMPLEMENTED_BY = {'Verb'}
    SPECIFIED_BY = {'Verb'}

    def python(self):
        return 'if_ {verb}:'.format(verb=self.complement.python())


class Verb(Word):
    """ Open class for lowercase, alphabetic, multi-character lexemes. """
    KEYWORDS = {'is', 'has'}
    PATTERN = r"[a-z][a-z]+"
    COMPLEMENTS = {'Noun'}

    def python(self):
        return '{specifier}.{head}{complement}'.format(
            specifier=python(self.specifier) or 'you',
            head=self.head + '_' * keyword.iskeyword(self.head) or '',
            complement=python(self.complement, prefix='(', suffix=')'),
        )


# This replaces the names in production rules with their values.
# This is needed in Python because of the lack of forward declaration.
for cls in Word.__subclasses__():
    cls.COMPLEMENTED_BY = {eval(name) for name in cls.COMPLEMENTED_BY}
    cls.SPECIFIES = {eval(name) for name in cls.SPECIFIES}
    cls.COMPLEMENTS = {eval(name) for name in cls.COMPLEMENTS}
    cls.SPECIFIED_BY = {eval(name) for name in cls.SPECIFIED_BY}
