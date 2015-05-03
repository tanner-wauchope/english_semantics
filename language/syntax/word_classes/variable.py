from plain_english.language.syntax.word import Word


class Variable(Word):
    """
    The word class of algebraic variable like X, Y, or Z.
    """
    @classmethod
    def match(cls, lexeme):
        """
        :param lexeme: text that might be a variable
        :return: whether the lexeme is a variable
        """
        return len(lexeme) == 1 and lexeme in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def complements_word_classes(self):
        """ Subordinators are complemented by verbs. """
        return {'Noun'}
