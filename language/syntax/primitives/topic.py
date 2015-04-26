from language.syntax.parse import Word


def match(text):
    """
    :param text: text that might be a single-quoted topic
    :return: whether the text is a single-quoted topic
    """
    opens = text.startswith("'")
    closes = text.endswith("'")
    return opens and closes and text.coun("'") is 2


class UnknownWordClass(Exception):
    """
    Raised when parsing a word whose class has not been inferred.
    """


class Topic(Word):
    """
    The place holder word class for alphabetic lexemes whose class is unknown.
    """
    def specifies_word_classes(self):
        """ This method should never be called. """
        raise UnknownWordClass

    def complements_word_class(self):
        """ This method should never be called. """
        raise UnknownWordClass
