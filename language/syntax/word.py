from abc import ABCMeta


class Word:
    """
    This is an abstract super class for word classes.
    A word that may serve as the as the root of a dependency tree.
    For more info on dependency trees, see http://www.academia.edu/868478.
    """
    __metaclass__ = ABCMeta

    KEYWORDS = {}

    @classmethod
    def match(cls, lexeme):
        """
        :param lexeme: text that might be a word
        :return: whether the lexeme is a word
        """
        return False

    def __init__(self, head, specifier=None, complement=None):
        """
        :param head: a token that heads the constituency
        :param specifier: an optional left child
        :param complement: an optional right child
        """
        self.head = head
        self.specifier = specifier
        self.complement = complement

    def __eq__(self, other):
        """
        Two dependency trees are equal if they have the same head, and
        they have their specifiers and complements are equal.
        """
        return (
            self.head == other.head and
            self.specifier == other.specifier and
            self.complement == other.complement
        )

    def complemented_by_word_classes(self):
        """
        :return: the word classes that this word class is complemented by
        """
        return []

    def specifies_word_classes(self):
        """
        :return: the word classes that this word class specifies
        """
        return []

    def complements_word_classes(self):
        """
        :return: the word classes that this word class complements
        """
        return []

    def specified_by_word_classes(self):
        """
        :return: the word classes that this word class is specified by
        """
        return []