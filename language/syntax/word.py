
class Word:
    """
    A word that may serve as the as the root of a dependency tree.
    For more info on dependency trees, see http://www.academia.edu/868478.
    """
    KEYWORDS = {}
    PATTERN = ''
    COMPLEMENTED_BY = {}
    SPECIFIES = {}
    COMPLEMENTS = {}
    SPECIFIED_BY = {}

    @classmethod
    def subclasses(cls):
        """
        Loads the subclass definitions if they are not already loaded.
        :return: a list of all the word classes
        """
        return cls.__subclasses__()

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
        their specifiers and complements are equal.
        """
        return (
            other and
            self.head == other.head and
            self.specifier == other.specifier and
            self.complement == other.complement
        )

