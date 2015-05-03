from plain_english.language.syntax.word import Word


class Possessive(Word):
    """
    The word class of inherently possessive words like 'it' and 'their'.
    """
    KEYWORDS = {
        'its',
        'their',
    }

    def specifies_word_classes(self):
        """ Possessives precede word_classes. """
        return {'Noun'}
