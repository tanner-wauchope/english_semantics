from language.syntax.word_classes.topic import Topic
from language.syntax.word_classes import word_classes


def first(tree):
    """
    :param tree: a binary tree of constituencies
    :return: the left-most node in the tree
    """
    if not tree.specifier:
        return tree
    return first(tree.specifier)


def last(tree):
    """
    :param tree: a binary tree of constituencies
    :return: the right-most node in the tree
    """
    if not tree.complement:
        return tree
    return last(tree.complement)


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
    for name in tree.specifies_word_classes():
        word_class = word_classes[name]
        if isinstance(other, word_class):
            return word_class


def complements(tree, other):
    """
    :param tree: a binary tree composed of constituencies
    :param other: a second binary tree of constituencies
    :return: the first word class the the second tree complements
    """
    for name in other.complements():
        word_class = word_classes(name)
        if isinstance(tree, word_class):
            return word_class


def merge(tree, other):
    """
    :param tree: a dependency tree of words
    :param other: a dependency tree of words
    :return: one of the trees, except with the other tree added as a subtree
    """
    if last(tree).complemented_by(other):
        last(tree).complement = other
        return tree
    elif tree.specifies(first(other)):
        first(other).specifier = tree
        return other
    elif other.complements(last(tree)):
        last(tree).complement = other
        return tree
    elif first(other).specified_by(tree):
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
        constituency = create_constituency(tokens.pop(0), tree)
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
