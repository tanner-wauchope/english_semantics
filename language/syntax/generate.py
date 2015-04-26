

def specifier(tree):
    """
    :param tree: a binary tree composed of constituencies
    :return: python for the left branch of the tree
             nothing is returned if there is no left branch
    """
    if tree.specifier:
        return generate(tree.specifier) + '.'
    return ''


def complement(tree):
    """
    :param tree: a binary tree composed of constituencies
    :return: python for the right branch of the tree
             nothing is returned if there is no right branch
    """
    if tree.complement:
        return '(' + generate(tree.complement) + ')'
    return ''


def generate(tree):
    """
    :param tree: a binary tree composed on constituencies
    :return: python whose execution tree mimics the input tree
    """
    return specifier(tree) + tree.head + complement(tree)
