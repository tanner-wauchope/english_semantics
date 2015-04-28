from language.syntax.word import Word


def subordinate(tree, quote):
    """
    :param tree: a binary tree composed of constituencies
    :return: python whose execution tree mimics the input tree
    """
    result = ''
    if tree.specifier:
        result += codify(tree.specifier, quote) + '.'
    result += tree.head + '_'
    if tree.complement:
        result += '(' + quote + codify(tree.complement, '\\"') + quote + ')'
    return result


def coordinate(block, quote):
    """
    :param tree: a list of constituencies
    :return: python that coordinates the constituencies
    """
    conjoins = []
    for tree in block:
        conjoins.append(codify(tree, '\\"'))
    return '_(' + quote + ', '.join(conjoins) + quote + ')'


def codify(english, quote='"'):
    """
    :param english: a block of english or a fragment of a block
    :return: python that represents the block or fragment
    """
    if isinstance(english, list):
        return coordinate(english, quote)
    elif isinstance(english, Word):
        return subordinate(english, quote)
