from . import package_name, Parser

class Interpreter:
    def __init__(self):
        self.parser = Parser()

    def line_prefix(self):
        if self.parser.has_last_line():
            print('>>> ')
        print('... ')

    def flush(self):
        try:
            return next(self.parser)
        except StopIteration:
            return ''

    def run(self):
        print(package_name)
        while True:
            print(self.line_prefix())
            self.parser.read(input())
            exec(self.parser.flush())
