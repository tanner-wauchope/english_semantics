import os

from parser import parse_line

def target_name(source_path):
    source_name = os.path.split(source_path)[-1]
    base = source_name.split(".")[0]
    return base + '.py'

def transfer(source, target):
    for line in source.readlines():
        print(parse_line(line), file=target)

def run_compiler(source_paths):
    for source_path in source_paths:
        with open(target_name(source_path), 'w') as target:
            with open(source_path, 'r') as source:
                transfer(source, target)

