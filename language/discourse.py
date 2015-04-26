from language.syntax import scan, tokenize, parse, generate, warn
from language.syntax.primitives.topic import Topic


def get_topic(tree):
    """
    :param tree: a binary tree of constituencies
    :return: the first topic found by depth-first search
    """
    if tree.head.word_class is Topic:
        return tree
    elif tree.specifier:
        return get_topic(tree.specifier)
    elif tree.complement:
        return get_topic(tree.complement)


class Discourse:
    """
    A discourse maintains inter-block state during interpretation.
    It tracks topics defined in previous paragraphs.
    It also keeps track of lines that have not yet formed a complete paragraph.
    """
    def __init__(self):
        """
        Initialize a dictionary to hold the topics of previous paragraphs.
        Initialize a buffer to hold lines of an incomplete paragraph.
        Expose language keywords to the Python runtime environment.
        """
        self.topics = {}
        self.paragraph = ''
        self.interpret('"from language import *"\n')
        self.interpret('\n')

    def interpret(self, line):
        """
        Save the line after removing invisible white space.
        If the line completes a paragraph, parse it and reset it.
        """
        self.paragraph += line.rstrip() + '\n'
        if self.paragraph.endswith('\n\n'):
            lexemes = scan(self.paragraph)
            tokens = tokenize(lexemes, self.topics)
            tree = parse(tokens)
            topic = get_topic(tree[0])
            self.topics[str(topic)] = topic
            self.paragraph = ''
            return generate(tree), warn(tree)
