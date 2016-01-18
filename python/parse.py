
class ParsingError(SyntaxError):
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
    raise ParsingError('Phrases cannot merge: ' + str([tree, other]))


def garden_path(tokens):
    """
    :param tokens: a list of tokens
    :return: a list of python trees
    """
    trees = tokens[:1]
    for token in tokens[1:]:
        try:
            trees[-1] = merge(trees[-1], token)
        except ParsingError:
            try:
                trees = garden_path(trees)
                trees[-1] = merge(trees[-1], token)
            except ParsingError:
                trees.append(token)
    if len(tokens) != len(trees):
        return garden_path(trees)
    else:
        return trees


def parse(block):
    """
    :param block: sentences that contain lines that contain tokens
    :return: a list of lists of binary trees that represent sentences
    """
    # TODO: delete the need for this
    sentences = []
    for sentence in block:
        phrases = []
        for phrase in sentence:
            new = garden_path(phrase)
            if len(new) == 1:
                phrases.append(new[0])
            else:
                raise ParsingError('Phrases cannot merge: ' + str(new))
        sentences.append(phrases)
    return sentences


# Experimental parser changes


def initialize_chart(tokens):
    total = len(tokens)
    chart = [[[] * total] * total]
    for i in range(total):
        for j in range(total):
            cell = chart[i][j]
            if i == j:
                cell.append(tokens[i])
            elif i > j:
                cell.append(None)
    return chart


def is_dependent(tree, other):
    """
    Minimal attachment takes precedence over late closure.
    :param tree: a binary-branching dependency tree of words
    :param other: a binary-branching dependency tree of words
    :return: whether tree can merge with other
    """
    return (
        contains(last(tree).COMPLEMENTED_BY, other) or
        contains(tree.SPECIFIES, first(other)) or
        contains(other.COMPLEMENTS, last(tree)) or
        contains(first(other).SPECIFIED_BY, tree)
    )


def dependents(candidates, parent) -> list:
    return [token for token in candidates if is_dependent(token, parent)]


def build_chart(tokens) -> list:
    """Alternative parser implementation based on CYK algorithm"""
    total = len(tokens)
    chart = initialize_chart(tokens)
    for start in range(1, total):
        for stop in range(start, total):
            for partition in range(start, stop - 1):
                head = tokens[partition]
                left = chart[start][partition - 1]
                right = chart[partition + 1][stop]
                if dependents(left, head) and dependents(right, head):
                    chart[start][stop].append(head)
    return chart


def trace(chart, i, j) -> 'Word':
    heads = chart[i][j]
    if len(heads) == 0:
        raise ParsingError('No valid parse: ' + str(chart))
    elif len(heads) > 1:
        raise ParsingError('Global ambiguity: ' + str(chart))

    head = heads[0]
    if head is None:
        return head

    if head.index > i:
        head.specifier = trace(chart, i, head.index - 1)
    if head.index < j:
        head.complement = trace(chart, head.index + 1, j)
    return head


def cyk_parse(tokens) -> 'Word':
    for i, token in enumerate(tokens):
        token.index = i
    chart = build_chart(tokens)
    return trace(chart, 0, len(tokens))