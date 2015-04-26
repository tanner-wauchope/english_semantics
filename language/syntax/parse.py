from language.syntax.primitives.topic import Topic


class Word:
    """
    The parse node for a word.
    The node may have a specifier or a complement.
    See http://www.academia.edu/868478.
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

    def specifies_word_classes(self):
        """
        :return: the word classes that this word class specifies
        """
        raise NotImplementedError

    def complements_word_class(self):
        """
        :return: the word classes that this word class complements
        """
        raise NotImplementedError


class PhrasesCannotMerge(Exception):
    """
    Thrown when two phrases cannot be merged.
    The first phrase cannot specify the second,
    and the second phrase cannot complement the first.
    """
    pass


def specifies(tree, other):
    """
    :param tree: a binary tree composed of constituencies
    :param other: a second binary tree of constituencies
    :return: the first word class the the first tree specifies
    """
    for word_class in tree.specifies_word_classes():
        if isinstance(other, word_class):
            return word_class

def complements(tree, other):
    """
    :param tree: a binary tree composed of constituencies
    :param other: a second binary tree of constituencies
    :return: the first word class the the second tree complements
    """
    for word_class in other.complements_word_classes():
        if isinstance(tree, word_class):
            return word_class


def merge(tree, other):
    """
    :param tree: a binary tree composed of constituencies
    :param other: a second binary tree of constituencies
    :return: a catena that subsumes these trees
    """
    if not last(tree).complement and other.complements(tree):
        last(tree).complement = other
        return tree
    elif not first(other).specifier and tree.specifies(other):
        first(other).specifier = tree
        return other
    raise PhrasesCannotMerge([tree, other])


def merge_or_move(tree, other):
    """
    :param other: a second binary tree of constituencies
    :return: the ordered merge or else the out-of-order merge
             the out-of-order merge allows for movement phenomena
    """
    try:
        return merge(tree, other)
    except PhrasesCannotMerge:
        return merge(other, tree)


def create_constituency(token, tree):
    """
    Reassign the token's word class based on the tree if its class is variable.
    :param constituency: a constituency that might need a word class
    :param tree: a binary tree composed of constituencies
    :return: an instantiation of the token's word class
    """
    if token.word_class is Topic:
        token.word_class = tree.head.word_class.specifies()
    return token.word_class(token.lexeme)


def garden_path(tokens):
    """
    :param tokens: a list of tokens
    :return: a binary syntax tree and any symbols that couldn't be assimilated
    """
    tree = create_constituency(tokens.pop(0), None)
    while tokens:
        constituency = create_constituency(tokens.pop(0))
        try:
            tree = merge(tree, constituency)
        except PhrasesCannotMerge:
            fork, constituencies = garden_path(tokens)
            tree = merge_or_move(tree, fork)
    return tree, tokens


def parse(block):
    """
    :param block: sentences that contain lines that contain tokens
    :return: a list of binary trees that represent sentences
    """
    for i, sentence in enumerate(block):
        for j, line in enumerate(sentence):
            sentence[j] = garden_path(line)[0]
        block[i] = garden_path(sentence)[0]
    return block
