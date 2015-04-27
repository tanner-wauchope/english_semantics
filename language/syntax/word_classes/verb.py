from language.syntax.word import Word


keywords = (
    'is',
    'has',
)


class Verb(Word):
    """
    The word class of alphabetic lexemes in positions that specify verbs.
    """
    def complements_word_classes(self):
        """ The verb of a relative clause complements a noun. """
        return ('Noun')