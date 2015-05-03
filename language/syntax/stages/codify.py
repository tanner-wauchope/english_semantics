def subordinate(tree):
    """
    :param tree: a binary tree composed of constituencies
    :return: python whose execution tree mimics the abstract syntax tree
    """
    result = tree.head.replace("'", '_') + '_'
    if tree.specifier and tree.specifier.index < tree.complement.index:
        result = result + subordinate(tree.specifier) + '.'
    if tree.complement:
        result += '(' + subordinate(tree.complement) + ')'
    if tree.specifier and tree.specifier.index > tree.complement.index:
        result += '(\n\t' + subordinate(tree.complement) + ')'
    return result


def coordinate(block):
    """
    :param block: a list of syntax trees
    :return: lazy python that coordinates the syntax trees
    """
    conjoins = []
    for tree in block:
        conjoins.append(subordinate(tree))
    return '_(\n\t"' + ',\n\t'.join(conjoins) + ',")'

def codify(trees):
    """
    :param trees: a list of syntax trees
    :return: python that represents the tree or list of trees
    """
    if len(trees) is 1:
        return subordinate(trees[0])
    return coordinate(trees)