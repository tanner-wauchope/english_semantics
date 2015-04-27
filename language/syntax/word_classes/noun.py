from language.syntax.word import Word


keywords = (
    'it',
    'number',
    'quote',
)


class Noun(Word):
    """
    The word class of alphabetic lexemes in positions that specify word_classes.
    """
    def specifies_word_classes(self):
        """ Nouns specify verbs. """
        return ('Verb')

    def complements_word_classes(self):
        """ Nouns complement verbs. """
        return ('Verb')

