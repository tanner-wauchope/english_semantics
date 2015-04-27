from language.syntax.word import Word


def match(text):
    """
    :param text: text that might be a single-quoted topic
    :return: whether the text is a single-quoted topic
    """
    parts = text.split("'")
    return len(parts) is 2 and parts[0].isalpha() and parts[1] in 's'


class Possessive(Word):
    """
    The word class of any alphabetic lexemes ending with "'" or "'s".
    """
    def specifies_word_classes(self):
        """ Possessives precede word_classes. """
        return ('Noun')

