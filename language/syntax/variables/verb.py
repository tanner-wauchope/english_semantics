from language.syntax.parse import Word
from language.syntax.variables import Noun
from language.syntax.variables.complementizer import Complementizer
from language.syntax.variables.subordinator import Subordinator


class Verb(Word):
    """
    The word class of alphabetic lexemes in positions that specify verbs.
    """
    def specifies_word_classes(self):
        """ Verbs specify subordinating conjunctions. """
        return [Subordinator]

    def complements_word_class(self):
        """ The verb of a relative clause complements a noun. """
        return [Noun, Complementizer]