import keyword

"""
It may be helpful to allow a plural number of specifiers and complements:
- This would allow coordination of nouns, predicates, clauses, and sentences.
"""
# TODO: I need to somehow verify that coordinated dependents are like-typed.


def count_prefix(prefix, sequence) -> int:
    for i, char in enumerate(sequence):
        if char not in prefix:
            return i
    return len(tuple(sequence))


class Tree:
    """
    A word that may serve as the as the root of a dependency tree.
    For more info on dependency trees, see http://www.academia.edu/868478.
    """
    KEYWORDS = {}
    PATTERN = None
    COMPLEMENTED_BY = {}
    SPECIFIES = {}
    COMPLEMENTS = {}
    SPECIFIED_BY = {}

    def __init__(self, head, specifier=None, complement=None, level=None):
        """
        :param head: a token that heads the constituency
        :param specifier: an optional left child
        :param complement: optional right children
        """
        self.head = head
        self.specifier = specifier or []
        self.complement = complement or []
        self.level = level
        self.index = 0

    def __eq__(self, other):
        """
        Two dependency trees are equal if they have the same head, and
        their specifiers and complements are equal.
        """
        return (
            isinstance(other, Tree) and
            self.head == other.head and
            self.specifier == other.specifier and
            self.complement == other.complement
        )

    def __str__(self):
        """
        :return: the english that this tree represents
        """
        result = []
        for tree in self.specifier:
            result.append(str(tree))
        result.append(self.head)
        for tree in self.complement:
            result.append(str(tree))
        return ' '.join(result)

    def python(self):
        raise NotImplementedError

    def children(self):
        result = []
        if self.specifier:
            result.append(self.specifier)
        if self.complement:
            result.append(self.complement)
        return result


def python(word, prefix='', suffix=''):
    if word is None:
        return ''
    else:
        return prefix + word.python() + suffix


class Clitic(Tree):
    """ The word class for possessive suffixes like "'" and "'s". """
    KEYWORDS = {"'s", "'"}
    SPECIFIES = {'Noun'}
    SPECIFIED_BY = {'Noun'}

    def python(self):
        return '{specifier}.'.format(specifier=self.specifier.python())


class Complementizer(Tree):
    """ The word class for the relative pronoun "that". """
    KEYWORDS = {'that'}
    COMPLEMENTED_BY = {'Verb'}
    COMPLEMENTS = {'Noun'}

    def python(self):
        return ''


class And(Tree):
    """ The word that tuples noun phrases. """
    KEYWORDS = {'and'}
    COMPLEMENTED_BY = {'Noun', 'Verb'}
    SPECIFIED_BY = {'Noun', 'Verb'}

    def python(self):
        return '{0} & {1}'.format(
            self.specifier.python(),
            self.complement.python(),
        )


class Or(Tree):
    """ Indicates a statement is a backup to the previous statement. """
    KEYWORDS = {'or'}
    COMPLEMENTED_BY = {'Noun', 'Verb'}
    SPECIFIED_BY = {'Noun', 'Verb'}

    def python(self):
        return 'else:'


class Determiner(Tree):
    """ The word class for articles and quantifiers. """
    KEYWORDS = {'an', 'a', 'the'}
    SPECIFIES = {'Noun'}

    def python(self):
        return ''


class Noun(Tree):
    """ Open class for capitalized, alphabetic, multi-character lexemes. """
    KEYWORDS = {'it', 'numbers', 'number', 'quotes', 'quote'}
    PATTERN = r'[A-Z][a-z]+[0-9]*'
    SPECIFIES = {'Verb'}
    COMPLEMENTS = {'Verb'}

    def python(self):
        return '{0}{1}{2}'.format(
            python(self.specifier),
            self.head.lower(),
            python(self.complement),
        )


class Number(Tree):
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


class Parenthetical(Tree):
    """ Comments, irregular form decorations, and embedded Python. """
    PATTERN = r'\(.+\)'
    COMPLEMENTS = {'Noun', 'Verb'}

    @staticmethod
    def valid(text):
        return (
            text[0] == '(' and
            text[-1] == ')' and
            text.count('(') == text.count(')')
        )

    def python(self):
        try:
            compile(self.head, '', 'eval')
            return self.head[1:-1]
        except SyntaxError:
            return ''


class Preposition(Tree):
    """ The class of prepositions. """
    KEYWORDS = {'of'}
    COMPLEMENTED_BY = {'Noun', 'Number'}
    COMPLEMENTS = {'Noun', 'Number'}

    def python(self):
        return '({noun_phrase})'.format(noun_phrase=self.complement.python())


class Quote(Tree):
    """
    The class for embedded quotations.
    The regular expression is from http://stackoverflow.com/questions/249791
    """
    PATTERN = r'"(?:[^"\\]|\\.)*"'
    COMPLEMENTS = {'Noun', 'Verb'}

    @staticmethod
    def valid(text) -> bool:
        backslashes = count_prefix('\\', reversed(text[:-1]))
        return (
            text[0] == '"' and
            text[-1] == '"' and
            len(text) > 1 and
            backslashes % 2 == 0
        )

    def python(self):
        return self.head


class Subordinator(Tree):
    """ The class of words that begin a subordinate clause. """
    KEYWORDS = {'if'}
    COMPLEMENTED_BY = {'Verb'}
    SPECIFIED_BY = {'Verb'}

    def python(self):
        return 'if_ {verb}:'.format(verb=self.complement.python())


class Verb(Tree):
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

# Experimental non-dependency items
# support article, noun, verb, subordinator, quote, preposition,
#  number, or, and, complementizer, clitic

# Verbs
class Sentence(Tree):
    rules = (
        ('CompoundingSentence', 'Sentence'),
        ('NounPhrase', 'Predicate'),
        ('SubordinateClause', 'Sentence'),
        ('Sentence', 'SubordinateClause'),
    )

class NounPhrase(Tree):
    rules = (
        ('Noun',),
        ('Primitive',),
        ('Determiner', 'Noun'),
        ('Noun', 'Primitive'),
        ('NounPhrase', 'PrepositionalPhrase'),
        ('NounPhrase', 'RelativeClause'),
        ('CompoundingNounPhrase', 'NounPhrase'),
    )

class VerbPhrase(Tree):
    rules = (
        ('Primitive'),
        ('Verb', 'NounPhrase'),
        ('CompoundingVerbPhrase', 'VerbPhrase'),
    )

class RelativeClause:
    rules = (
        ('That', 'VerbPhrase'),
        ('That', 'Sentence'),
    )

# *, /, of
class PrepositionalPhrase:
    rules = (
        ('*', 'NounPhrase'),
        ('/', 'NounPhrase'),
        ('of', 'NounPhrase'),
    )

# Conjunctions
class Paragraph:
    rules = (
        ('Sentence', 'Sentence')
    )

class CompoundingVerbPhrase:
    rules = (
        ('And', 'VerbPhrase')
    )

class CompoundingNounPhrase:
    rules = (
        ('Or', 'NounPhrase')
    )

class CompoundingSentence:
    rules = (
        ('Sentence', 'And')
    )

# Conditions
class SubordinateClause:
    rules = (
        ('Subordinator', 'Sentence')
    )


class ConjunctiveAdverbialPhrase:
    rules = (
        ('Or', 'SubordinateClause')
    )

# 's
class Possessive:
    rules = (
        ('NounPhrase', 'Clitic')
    )

#TODO: should read rules out of a file here and attach them to the classes
# This replaces the names in production rules with their values.
# This is needed in Python because of the lack of forward declaration.
categories = Tree.__subclasses__()
for cls in categories:
    cls.COMPLEMENTED_BY = {eval(name) for name in cls.COMPLEMENTED_BY}
    cls.SPECIFIES = {eval(name) for name in cls.SPECIFIES}
    cls.COMPLEMENTS = {eval(name) for name in cls.COMPLEMENTS}
    cls.SPECIFIED_BY = {eval(name) for name in cls.SPECIFIED_BY}
