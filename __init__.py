import sys

from interpreter import run_interpreter
from compiler import run_compiler

version = '0.1'

if __name__ == "__main__":
    file_paths = sys.argv[1:]
    if file_paths:
        run_compiler(file_paths)
    else:
        run_interpreter()