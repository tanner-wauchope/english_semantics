import sys

from . import package_name, parse_block


def run_interpreter():
    print(package_name + '\n' + '>>> ')
    block = []
    while True:
        line = input()
        block.append(line)
        if line.isspace():
            exec(parse_block(block))
            print('>>> ')
        else:
            print('... ')


def run_compiler(source_path):
    block = []
    with open(source_path.replace('.english', 'lexer.py'), 'w') as target:
        print('# ' + package_name, file=target)
        print('from english_semantics.words import *\n', file=target)
        with open(source_path, 'r') as source:
            for line in source.readlines():
                block.append(line)
                if line.isspace():
                    print(parse_block(block), file=target)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    if len(arguments) is 0:
        run_interpreter()
    elif len(arguments) is 1 and not arguments[0].startswith('-h'):
        run_compiler(arguments[0])
    else:
        print('Provide zero arguments to run the interpreter.')
        print('Provide a file path to run the compiler.')