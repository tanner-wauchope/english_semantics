from argparse import ArgumentParser
from os.path import getmtime

from plain_english.python.compiler import Compiler


def get_file(help_message):
    parser = ArgumentParser()
    parser.add_argument('file', type=open, help=help_message)
    args = parser.parse_args()
    return args.file


def last_modified(file_path):
    try:
        return getmtime(file_path)
    except FileNotFoundError:
        return 0


def main():
    english = get_file("English to be compiled to Python")
    python = english.name.split('.')[0] + '.py'
    if last_modified(english) > last_modified(python):
        compiler = Compiler(english)
        compiler.run()
    exec(open(python).read())
