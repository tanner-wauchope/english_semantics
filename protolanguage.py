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
    def __repr__(self): return self.name + str(id(self))


def tokenize(lexemes, variables):
    lexemes = list(lexemes)
    variables = dict(variables)
    for i, lexeme in enumerate(lexemes):
        if lexeme[0].isupper():
            if lexeme in variables:
                lexemes[i] = variables[lexeme]
            else:
                variables[lexeme] = Variable(lexeme)
                lexemes[i] = variables[lexeme]
    return tuple(lexemes), variables


def parse(block):
    results = []
    variables = {}
    for statement in block:
        lexemes, variables = tokenize(statement, variables)
        results.append(lexemes)
    return results[0], results[1:], variables


def guess_variable(consumer, consumed, scope):
    if isinstance(consumer[0], Variable):
        for i in range(1, len(consumed) + 1):
            if isinstance(consumed[i - 1], Variable):
                return
            proposal = {**scope, **{consumer[0]: consumed[:i]}}
            yield from unify(consumer[1:], consumed[i:], proposal)


def interpolate(statement, scope):
    result = []
    for token in statement:
        if token in scope:
            result.extend(interpolate(scope[token], scope))
        else:
            result.append(token)
    return tuple(result)


def unify(statement1, statement2, scope):
    statement1 = interpolate(statement1, scope)
    statement2 = interpolate(statement2, scope)
    if statement1 == statement2 == ():
        yield scope
    elif () in (statement1, statement2):
        return
    elif statement1[0] == statement2[0]:
        yield from unify(statement1[1:], statement2[1:], scope)
    elif isinstance(statement1[0], Variable) and isinstance(statement2[0], Variable):
        proposal = {**scope, **{statement1[0]: statement2[:1]}}
        yield from unify(statement1[1:], statement2[1:], proposal)
    else:
        yield from guess_variable(statement1, statement2, scope)
        yield from guess_variable(statement2, statement1, scope)


def match(query, statement):
    def goal(scope):
        yield from unify(query, statement, scope)
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
                head, body, _ = parse(db[key])
                goals.append(conj(match(statement, head), definition(body, db)))
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
        # task: preserve whitespace from initial string - matters for punctuated sentences
        result = ' '.join(str(x) for x in interpolate(query, scope)) + '\n'
        if result not in seen:
            seen.add(result)
            yield result


def debug(message, items):
    if len(sys.argv) == 2 and sys.argv[1] == 'debug' and items:
        print(message + ':')
        for item in items:
            print('  ' + str(item))


def run(block, db):
    if block:
        head, body, variables = parse(block)
        if body:
            db[head] = block
        elif variables:
            query = search(head, db)
            stream =  list(query({}))
            debug('Stream', stream)
            return ''.join(get_lines(head, stream))
        else:
            db[head] = True
    return ''


def main(db=None):
    if db is None:
        db = collections.OrderedDict()
    print("Protolanguage (Version 0)")
    while True:
        lines = [lex(input('>>> '))]
        while lines[-1]:
            lines.append(tuple(lex(input('... '))))
        print(run(lines[:-1], db), end='')
        debug('DB', db.items())


if __name__ == '__main__':
    main()
