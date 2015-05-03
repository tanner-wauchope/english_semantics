from plain_english.language.syntax.word import Word


class Verb(Word):
    """
    The word class of alphabetic lexemes in positions that specify verbs.
    """
    KEYWORDS = {
        'is',
        'has',
    }

    def complements_word_classes(self):
        """ The verb of a relative clause complements a noun. """
        return {'Noun'}

    @classmethod
    def match(cls, lexeme):
        """
        A verb is alphabetic, lowercase, and possibly single-quoted.
        """
        if lexeme.count('"') is 2 and lexeme[0] == '"' and lexeme[-1] == '"':
            lexeme = lexeme[1:-1]
        return lexeme.isalpha() and lexeme.islower()
