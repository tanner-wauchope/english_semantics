from language.syntax.stages.parse import Word


def match(text):
    """
    :param text: text that might be a single-quoted topic
    :return: whether the text is a single-quoted topic
    """
    opens = text.startswith("'")
    closes = text.endswith("'")
    return opens and closes and text.coun("'") is 2


class Topic(Word):
    """
    The place holder word class for alphabetic lexemes whose class is unknown.
    """
    def complemented_by_word_classes(self):
        """ This method should never be called. """
        raise NotImplementedError

    def specifies_word_classes(self):
        """ This method should never be called. """
        raise NotImplementedError

    def complements_word_classes(self):
        """ This method should never be called. """
        raise NotImplementedError

    def specified_by_word_classes(self):
        """ This method should never be called. """
        raise NotImplementedError
