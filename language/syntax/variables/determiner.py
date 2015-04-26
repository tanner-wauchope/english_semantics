from language.syntax.parse import Word
from . import Noun


class Determiner(Word):
    """
    The word class of articles and quantifiers like "each" and "every"
    """
    def specifies_word_classes(self):
        """ Determiners specify variables. """
        return [Noun]

    def complements_word_class(self):
        """ Determiners do not complement anything. """
        return []

