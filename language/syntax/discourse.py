from .stages import scan, tokenize, parse, generate_code, warn
from .word_classes.topic import Topic


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


def interpret(english, topics={}):
    lexemes = scan(english)
    tokens = tokenize(lexemes, topics)
    tree = parse(tokens)
    topic = get_topic(tree[0])
    topics[str(topic)] = topic
    return generate_code(tree)


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
            interpretation = interpret(self.paragraph, self.topics)
            self.paragraph = ''
            return interpretation
