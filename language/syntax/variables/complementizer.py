from language.syntax.parse import Word
from . import Noun


class Complementizer(Word):
    """
    The word class of keywords like "that" and "whose"
    """
    def specifies_word_classes(self):
        """ Determiners do not complement anything. """
        return []

    def complements_word_class(self):
        """ Complementizers complement variables. """
        return [Noun]

