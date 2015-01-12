from . import version
from parser import parse_line

def print_prefix(line):
    if line.strip():
        print("...", end=' ')
    else:
        print(">>>", end=' ')

def run_interpreter():
    print("Poesy " + version)
    line = ""
    while True:
        print_prefix(line)
        line = input()
        exec(parse_line(line))
