class Word:
    """
    A word that may serve as the as the root of a dependency tree.
    For more info on dependency trees, see http://www.academia.edu/868478.
    """
    def __init__(self, head, specifier=None, complement=None):
        """
        :param head: a token that heads the constituency
        :param specifier: an optional left child
        :param complement: an optional right child
        """
        self.head = head
        self.specifier = specifier
        self.complement = complement

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