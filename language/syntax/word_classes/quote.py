from plain_english.language.syntax.word import Word


def match(text):
    """
    :param text: text that might be a double-quoted quote
    :return: whether the text is a double-quoted quote
    """
    opens = text.startswith('"')
    closes = text.endswith('"')
    return opens and closes and text.count('"') is 2


class Quote(Word):
    """
    The word class of any alphabetic lexemes wrapped in '"'.
    """
    def complements_word_classes(self):
        """ Quotes follow nouns or verbs. """
        return ('Noun', 'Verb')


