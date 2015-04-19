import warnings

from language.syntax.common import WordClass
from language.syntax.nouns import Noun


class A(WordClass):
    def specifies(self, first, second):
        if second.head.spelling.startswith('aeiou'):
            warnings.warn('The word "a" should precede a consonant.')
        return isinstance(second.head.type, Noun)

class An(WordClass):
    def specifies(self, first, second):
        if not second.head.spelling.startswith('aeiou'):
            warnings.warn('The word "an" should precede a vowel.')
        return isinstance(second.head.type, Noun)

class The(WordClass):
    def specifies(self, first, second):
        return isinstance(second.head.type, Noun)
