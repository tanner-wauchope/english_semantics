
class PhrasesCannotMerge(Exception):
    """
    Thrown when two phrases cannot be merged.
    The first phrase cannot specify the second,
    and the second phrase cannot complement the first.
    """
    pass


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


def contains(word_classes, word):
    """
    :param word_class: a set of word classes
    :param word: a word that could be an instance of the word classes
    :return: whether the word is an instance of any of the word classes
    """
    for word_class in word_classes:
        if isinstance(word, word_class):
            return True


def merge(tree, other):
    """
    Minimal attachment takes precedence over late closure.
    :param tree: a binary-branching dependency tree of words
    :param other: a binary-branching dependency tree of words
    :return: one of the trees, except with the other tree added as a subtree
    """
    if contains(last(tree).COMPLEMENTED_BY, other):
        last(tree).complement = other
        return tree
    elif contains(tree.SPECIFIES, first(other)):
        first(other).specifier = tree
        return other
    elif contains(other.COMPLEMENTS, last(tree)):
        last(tree).complement = other
        return tree
    elif contains(first(other).SPECIFIED_BY, tree):
        first(other).specifier = tree
        return other
    raise PhrasesCannotMerge([tree, other])


def move(tree, other):
    """
    :param tree: a binary tree of tokens
    :param other: a second binary tree of tokens
    :return: an out-of-order merge of the trees
    """
    return merge(other, tree)


def garden_path(tokens, combine=merge):
    """
    :param tokens: a list of tokens
    :return: a binary syntax tree and any symbols that couldn't be assimilated
    """
    tree = tokens.pop(0)
    while tokens:
        token = tokens.pop(0)
        try:
            tree = merge(tree, token)
        except PhrasesCannotMerge:
            tokens.insert(0, token)
            fork, tokens = garden_path(tokens)
            tree = combine(tree, fork)
    return tree, tokens


def parse(block):
    """
    :param block: sentences that contain lines that contain tokens
    :return: a list of binary trees that represent sentences
    """
    sentences = []
    for sentence in block:
        clauses = []
        for clause in sentence:
            clauses.append(garden_path(clause)[0])
        sentences.append(garden_path(clauses, move)[0])
    return sentences
