import collections

from language.syntax import scan, tokenize, parse


class Discourse:
    def __init__(self):
        """
        Initialize a dictionary to hold paragraph topics.
        Expose language keywords to the Python runtime environment.
        """
        self.topics = collections.OrderedDict()
        self.paragraph = ''
        self.interpret('"from language import *"\n')
        self.interpret('\n')

    def flush(self):
        """
        Add the first topic of the paragraph to the global scope.
        Then, reset the paragraph before return it.
        """
        result = self.paragraph
        topic = result.scope.popitem(last=False)
        self.topics[topic[0]] = topic[1]
        self.paragraph = ''
        return result

    def interpret(self, line):
        """
        Save the line after removing invisible white space.
        If the line completes a paragraph, return the paragraph.
        """
        self.paragraph += line.rstrip() + '\n'
        if self.paragraph.endswith('\n\n'):
            self.paragraph = scan(self.paragraph)
            self.paragraph = tokenize(self.paragraph)
            self.paragraph = parse(self.paragraph)
            return self.flush()
