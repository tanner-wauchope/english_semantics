from plain_english.language.syntax.word import Word


keywords = (
    'it',
    'number',
    'quote',
)


def match(lexeme):
    """
    If a token is otherwise uncategorizable,
    assume it is a noun if it is alphabetic and capitalized.
    """
    return lexeme.isalpha() and lexeme.istitle()


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

