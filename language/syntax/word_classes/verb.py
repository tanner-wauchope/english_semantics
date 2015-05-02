from language.syntax.word import Word


keywords = (
    'is',
    'has',
)


def match(lexeme):
    """
    If a token is otherwise uncategorizable,
    assume it is a verb if it is alphabetic and lowercase.
    """
    return lexeme.isalpha() and lexeme.islower()


class Verb(Word):
    """
    The word class of alphabetic lexemes in positions that specify verbs.
    """
    def complements_word_classes(self):
        """ The verb of a relative clause complements a noun. """
        return ('Noun')