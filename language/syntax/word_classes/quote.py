from plain_english.language.syntax.word import Word


class Quote(Word):
    """
    The word class of any alphabetic lexemes wrapped in '"'.
    """
    @classmethod
    def match(cls, lexeme):
        """
        :param lexeme: text that might be a double-quoted quote
        :return: whether the lexeme is a double-quoted quote
        """
        opens = lexeme.startswith('"')
        closes = lexeme.endswith('"')
        return lexeme.count('"') is 2 and opens and closes

    def complements_word_classes(self):
        """ Quotes follow nouns or verbs. """
        return {'Noun', 'Verb'}
