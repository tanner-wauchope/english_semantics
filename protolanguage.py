import collections
import functools
import itertools
import re
import sys


def lex(line):
    return [t for t in re.split(r'(\W)', line) if t and not t.isspace()]


class Variable:
    def __init__(self, name): self.name = name
    def __str__(self): return self.name


def tokenize(lexemes, scope):
    for i, lexeme in enumerate(lexemes):
        if lexeme[0].isupper():
            if lexeme in scope:
                lexemes[i] = scope[lexeme]
            else:
                scope[lexeme] = Variable(lexeme)
                lexemes[i] = scope[lexeme]


def guess_var(consumer, consumed):
    if isinstance(consumer[0], Variable):
        for i in range(1, len(consumed) + 1):
            for scope in unify(consumer[1:], consumed[i:]):
                yield {**{consumer[0]: consumed[:i]}, **scope}


def unify(statement1, statement2):
    if statement1 == statement2 == ():
        yield {}
    elif () in (statement1, statement2):
        return
    elif statement1[0] == statement2[0]:
        yield from unify(statement1[1:], statement2[1:])
    else:
        yield from guess_var(statement1, statement2)
        yield from guess_var(statement2, statement1)


def interpolate(statement, scope):
    result = []
    for token in statement:
        if token in scope:
            result.extend(interpolate(scope[token], scope))
        else:
            result.append(token)
    return tuple(result)


def match(query, statement):
    def goal(scope):
        statement1 = interpolate(query, scope)
        statement2 = interpolate(statement, scope)
        yield from unify(statement1, statement2)
    return goal


def disj(*goals):
    return lambda scope: itertools.chain(*(goal(scope) for goal in goals))


def search(statement, db):
    def goal(scope):
        goals = []
        for key in db:
            if db[key] is True:
                goals.append(match(statement, key))
            else:
                goals.append(conj(match(statement, key), db[key]))
        return functools.reduce(disj, goals, lambda x: ())(scope)
    return goal


def conj(goal1, goal2):
    def goal(scope):
        intermediate = goal1(scope)
        return itertools.chain(*map(goal2, intermediate))
    return goal


def definition(conjuncts, db):
    goals = (search(conjunct, db) for conjunct in conjuncts)
    return functools.reduce(conj, goals)


def get_lines(query, scopes):
    seen = set()
    for scope in scopes:
        result = ' '.join(str(x) for x in interpolate(query, scope)) + '\n'
        if result not in seen:
            seen.add(result)
            yield result



def run(block, db, scope):
    for lexemes in block: tokenize(lexemes, scope)
    head = tuple(block[0])
    if block and db.get(head) is not True:
        if len(block) > 1:
            db[head] = definition(block[1:], db)
        elif scope:
            return ''.join(get_lines(head, search(head, db)({})))
        else:
            db[head] = True
    return ''


def main():
    db = collections.OrderedDict()
    print("Protolanguage (Version 0)")
    while True:
        lines = [lex(input('>>> '))]
        while lines[-1]: lines.append(lex(input('... ')))
        print(run(lines[:-1], db, {}), end='')
        if len(sys.argv) == 2 and sys.argv[1] == 'debug': print(db)


if __name__ == '__main__':
    main()
