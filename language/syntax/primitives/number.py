from language.syntax.parse import Word
from language.syntax.variables import Noun
from language.syntax.verbs import Verb


def match(text):
    """
    :param text: text that might be a floating-point number
    :return: whether the text is a floating-point number
    """
    try:
        return float(text)
    except ValueError:
        return None


class Number(Word):
    """
    The word class of spelled numbers and lexemes that can be cast as a float.
    """
    def specifies_word_classes(self):
        """ Numbers can precede variables. """
        return [Noun]

    def complements_word_class(self):
        """ Numbers can follow verbs. """
        return [Verb]
