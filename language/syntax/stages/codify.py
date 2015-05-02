from language.syntax.word import Word


def subordinate(tree, quote):
    """
    :param tree: a binary tree composed of constituencies
    :return: python whose execution tree mimics the abstract syntax tree
    """
    result = tree.head + '_'
    if tree.specifier and tree.specifier.index < tree.complement.index:
        result = result + codify(tree.specifier, quote) + '.'
    if tree.complement:
        result += '(' + quote + codify(tree.complement, '\\"') + quote + ')'
    if tree.specifier and tree.specifier.index > tree.complement.index:
        result += '(' + quote + codify(tree.complement, '\\"') + quote + ')'
    return result


def coordinate(block, quote):
    """
    :param tree: a list of syntax trees
    :return: python that coordinates the syntax trees
    """
    conjoins = []
    for tree in block:
        conjoins.append(codify(tree, quote))
    return '_(' + quote + ',\n\t'.join(conjoins) + quote + ')'


def codify(english, quote='"'):
    """
    :param english: a syntax tree or a list of syntax trees
    :return: python that represents the block or fragment
    """
    if isinstance(english, list):
        return coordinate(english, quote)
    elif isinstance(english, Word):
        return subordinate(english, quote)
