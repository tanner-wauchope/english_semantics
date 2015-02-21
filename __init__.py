import sys

from parser import Parser
from interpreter import Interpreter
from compiler import Compiler
from patterns import Pattern

package_name = 'English Semantics 0.1'

if __name__ == "__main__":
    file_paths = sys.argv[1:]
    if file_paths:
        Compiler(file_paths).run()
    else:
        Interpreter().run()