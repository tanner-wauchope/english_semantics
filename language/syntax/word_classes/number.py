from plain_english.language.syntax.word import Word


class Number(Word):
    """
    The word class of spelled numbers and lexemes that can be cast as a float.
    """
    KEYWORDS = {
        'zero',
        'one',
        'two',
        'three',
        'four',
        'five',
        'six',
        'seven',
        'eight',
        'nine',
    }

    @classmethod
    def match(cls, lexeme):
        """
        :param lexeme: text that might be a number
        :return: whether the lexeme is a number
        """
        try:
            return float(lexeme)
        except ValueError:
            return None

    def specifies_word_classes(self):
        """ Numbers can precede word_classes. """
        return {'Noun'}

    def complements_word_classes(self):
        """ Numbers can follow verbs. """
        return {'Verb'}
