import sys

from language.syntax.discourse import Discourse


def handle_error(path, line, error):
    message = (
        'file {path}, line {line}\n'
        '{type}: {description}'
    ).format(
        path=path,
        line=line,
        type=type(error),
        description=error.message,
    )
    print(message, sys.stderr)
    exit()

class Compiler:
    """
    A compiler translates source text into Python.
    The source text is specified as a path to a file with type ".en".
    To compiler is invoked with the "run" method.
    """
    def __init__(self, path):
        """
        Save the path to the file to be parsed.
        Initialize a buffer for lines that cannot be interpreted individually.
        """
        self.path = path
        self.discourse = Discourse()

    def interpretations(self):
        """
        Read each interpretable unit of the source code.
        """
        with open(self.path) as source:
            for i, line in enumerate(source):
                interpretation = self.discourse.interpret(line)
                if interpretation:
                    yield i, interpretation
        raise StopIteration

    def run(self):
        """
        Write each interpretable unit of the target code.
        """
        with open(self.path + '.py', 'w') as target:
            print('"from language import *"\n', file=target)
            for line, interpretation in self.interpretations():
                if isinstance(interpretation, Exception):
                    handle_error(self.path, line, interpretation)
                else:
                    print(str(interpretation), file=target, end='')
        print('Compilation succeeded.')
