import os

from . import package_name, Parser

def get_target_name(source_path):
    source_name = os.path.split(source_path)[-1]
    base = source_name.split(".")[0]
    return base + '.py'

class Compiler(Parser):
    def __init__(self, source_paths=[]):
        self.source_paths = source_paths
        self.parser = Parser()

    def read(self, source_path):
        with open(source_path, 'r') as source:
            for line in source.readlines():
                self.parser.read(line)

    def write(self, target_name):
        print('# ' + package_name)
        with open(target_name, 'w') as target:
            for parse in self.parser:
                print(parse, file=target)

    def run(self):
        while self.source_paths:
            source_path = self.source_paths.pop()
            self.read(source_path)
            self.write(get_target_name(source_path))
