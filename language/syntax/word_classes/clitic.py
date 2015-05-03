from plain_english.language.syntax.word import Word


class Clitic(Word):
    """
    The word class of keywords like "'" or "'s".
    """
    KEYWORDS = {
        "'",
        "'s",
    }

    def specifies_word_classes(self):
        """ Clitics precede nouns. """
        return {'Noun'}

    def specified_by_word_classes(self):
        """ Clitics optionally follow nouns. """
        return {'Noun'}
