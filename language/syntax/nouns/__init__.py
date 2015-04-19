from language.syntax.common import WordClass
from language.syntax.verbs import Verb


class Noun(WordClass):
    def specifies(self, first, second):
        return isinstance(second.head.word_class, Verb)

    def complements(self, second, first):
        return isinstance(first.head.word_class, Verb)

