import sys
from translator import parse

package_name = 'English Semantics 0.1'

def run_interpreter():
    print(package_name)
    print('>>> ', end='')
    block = []
    line = ''
    while True:
        line = input()
        block.append(line)
        if not line.strip():
            exec(parse(block))
            print('>>> ', end='')
        else:
            print('... ', end='')


def run_compiler(source_path):
    block = []
    output_path = source_path.replace('.english', '.py')
    with open(output_path, 'w') as target:
        print('# ' + package_name, file=target)
        print('from plain_english.semantics import *\n', file=target)
        with open(source_path, 'r') as source:
            for line in source.readlines():
                block.append(line)
                if line.isspace():
                    print(parse(block), file=target)
    print('Compilation succeeded.')
    print('The output was written to ' + output_path)


def main(*arguments):
    arguments = arguments or sys.argv[1:]
    if len(arguments) is 0:
        run_interpreter()
    elif len(arguments) is 1 and not arguments[0].startswith('-h'):
        run_compiler(arguments[0])
    else:
        print('Provide no arguments to run the interpreter.')
        print('Provide a file path to run the compiler.')

main()
