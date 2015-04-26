from language.syntax.parse import Word
from language.syntax.variables.verb import Verb


class Noun(Word):
    """
    The word class of alphabetic lexemes in positions that specify variables.
    """
    def specifies_word_classes(self):
        """ Nouns specify verbs. """
        return [Verb]

    def complements_word_class(self):
        """ Nouns complement verbs. """
        return [Verb]

