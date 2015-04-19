from language.discourse import Discourse


class Compiler:
    def __init__(self, path):
        self.path = path
        self.discourse = Discourse()

    def interpretations(self):
        with open(self.path) as source:
            for line in source:
                yield self.discourse.interpret(line)
        raise StopIteration

    def run(self):
        with open(self.path + '.py', 'w') as target:
            for interpretation in self.interpretations():
                print(str(interpretation), file=target, end='')
        print('Compilation succeeded.')
