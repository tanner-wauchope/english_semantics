from language.syntax.parse import Word
from language.syntax.variables import Noun
from language.syntax.verbs import Verb


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
    def specifies_word_classes(self):
        """ Quotes do not specify anything. """
        return []

    def complements_word_class(self):
        """ Quotes follow variables or verbs. """
        return [Noun, Verb]


