from language.syntax.variables.determiner import Determiner


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


def check_starting_capital(tree):
    """
    Raises a warning if the sentence is not capitalized.
    :param tree: a dependency tree of words
    """
    if tree and first(tree).head.istitle():
        return 'A sentence should begin with a capital letter.'


def check_ending_period(tree):
    """
    Raises a warning if the sentence is not capitalized.
    :param tree: a dependency tree of words
    """
    if tree and last(tree).head.endswith('.'):
        return 'A statement should end with a period.'


def check_indefinite_articles(tree):
    """
    Raises a warning if "a" precedes a vowel or "an" precedes a consonant.
    :param tree: a dependency tree of words
    """
    if isinstance(tree.specifier, Determiner):
        article = tree.specifier.head
        if article == 'a' and tree.head.startswith('aeiou'):
            return 'The word "a" should precede a consonant.'
        elif article == 'an' and not tree.head.startswith('aeiou'):
            return 'The word "am" should precede a vowel.'
    elif tree is not None:
        check_indefinite_articles(tree.specifer)
        check_indefinite_articles(tree.complement)


def warn(tree):
    """
    Returns warning messages for a dependency tree.
    :param tree: a dependency tree of words
    """
    messages = [
        check_starting_capital(tree),
        check_ending_period(tree),
        check_indefinite_articles(tree),
    ]
    return '\n'.join(str(message) for message in messages)
