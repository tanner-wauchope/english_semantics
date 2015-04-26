from warnings import warn_explicit

from language.discourse import Discourse


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
                interpretation, warning = self.discourse.interpret(line)
                if interpretation:
                    yield interpretation, i, warning
        raise StopIteration

    def run(self):
        """
        Write each interpretable unit of the target code.
        """
        with open(self.path + '.py', 'w') as target:
            for interpretation, line, warning in self.interpretations():
                print(str(interpretation), file=target, end='')
                if warning:
                    warn_explicit(warning, SyntaxWarning, self.path, line)
        print('Compilation succeeded.')
