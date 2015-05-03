from plain_english.language.syntax.word import Word


class Noun(Word):
    """
    The word class of alphabetic lexemes in positions that specify word_classes.
    """
    KEYWORDS = {
        'it',
        'number',
        'quote',
    }

    @classmethod
    def match(cls, lexeme):
        """
        A noun is alphabetic, lowercase, and possibly single-quoted.
        """
        if lexeme.count('"') is 2 and lexeme[0] == '"' and lexeme[-1] == '"':
            lexeme = lexeme[1:-1]
        return lexeme.isalpha() and lexeme.istitle()

    def specifies_word_classes(self):
        """ Nouns specify verbs. """
        return {'Verb'}

    def complements_word_classes(self):
        """ Nouns complement verbs. """
        return {'Verb'}
