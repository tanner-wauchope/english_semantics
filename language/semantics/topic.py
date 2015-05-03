def get_topic(tree):
    """
    :param tree: a binary tree of constituencies
    :return: the first topic found by depth-first search
    """
    if isinstance(tree, Topic):
        return tree
    elif tree.specifier:
        return get_topic(tree.specifier)
    elif tree.complement:
        return get_topic(tree.complement)