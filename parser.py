from semantics import Constituency

from lexer import tokenize

def parse(block):
    result = ''
    for line in block:
        words = []
        constituencies = []
        for token in tokenize(line):
            words.append(token)
            constituencies.append(Constituency(token))
            constituencies = unify(constituencies)
        result += repr(constituencies[0]) + '\n'
    return result

def unify(constituencies):
    combination = True
    while len(constituencies) > 1 and combination:
        second_to_last, last = constituencies[-2:]
        combination = second_to_last.combine(last)
        if combination:
            constituencies[:-2] = [combination]
    return constituencies
