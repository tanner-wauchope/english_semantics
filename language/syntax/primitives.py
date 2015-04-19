# cardinals ordinals

from language.syntax.common import WordClass


class Number(WordClass):
    def specifies(self, first, second):
        return (
            isinstance(second.head.type, Noun) or
            isinstance(second.head.type, Verb)
        )

    def complements(self, second, first):
        return isinstance(first.head.type, Noun)

# symbols quotes

from language.syntax.common import WordClass
from language.syntax.nouns import Noun
from language.syntax.verbs import Verb


class String(WordClass):
    def specifies(self, first, second):
        return isinstance(second.head.type, Verb)

    def complements(self, second, first):
        return isinstance(first.head.type, Noun)

