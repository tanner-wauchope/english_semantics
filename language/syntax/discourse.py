from .stages import scan, tokenize, parse, codify


def interpret(english):
    try:
        lexemes = scan(english)
        tokens = tokenize(lexemes)
        trees = parse(tokens)
        return codify(trees)
    except Exception as e:
        return e


class Discourse:
    """
    Keeps track of lines that have not yet formed a complete paragraph
    """
    def __init__(self):
        """
        Initialize a buffer to hold lines of an incomplete paragraph.
        """
        self.paragraph = ''

    def interpret(self, line):
        """
        Save the line after removing invisible white space.
        If the line completes a paragraph, parse it and reset it.
        """
        self.paragraph += line.rstrip() + '\n'
        if self.paragraph.endswith('\n\n'):
            interpretation = interpret(self.paragraph)
            self.paragraph = ''
            return interpretation
