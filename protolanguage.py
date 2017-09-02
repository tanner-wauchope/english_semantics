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


def unify(consumer, consumed, scope):
    consumer = interpolate(consumer, scope)
    consumed = interpolate(consumed, scope)
    if consumer == consumed == ():
        yield scope
    elif () in (consumer, consumed):
        return
    elif consumer[0] == consumed[0]:
        yield from unify(consumer[1:], consumed[1:], scope)
    elif isinstance(consumer[0], Variable) and isinstance(consumed[0], Variable):
        proposal = {**scope, **{consumer[0]: consumed[:1]}}
        yield from unify(consumer[1:], consumed[1:], proposal)
    else:
        yield from guess_variable(consumer, consumed, scope)


def match(consumer, consumed):
    def goal(scope):
        yield from unify(consumer, consumed, scope)
    return goal


def conj(goal1, goal2):
    def goal(scope):
        intermediate = goal1(scope)
        return itertools.chain.from_iterable(map(goal2, intermediate))
    return goal


def disj(*goals):
    return lambda scope: itertools.chain.from_iterable(goal(scope) for goal in goals)


def definition(conjuncts, db):
    goals = (search(conjunct, db) for conjunct in conjuncts)
    return functools.reduce(conj, goals)


def search(statement, db):
    def goal(scope):
        goals = []
        for key in db:
            if db[key] is True:
                goals.append(match(statement, key))
            else:
                head, body, _ = parse(db[key])
                goals.append(conj(match(head, statement), definition(body, db)))
        return functools.reduce(disj, goals, lambda x: ())(scope)
    return goal


def get_line(tokens, scope):
    return ' '.join(str(x) for x in interpolate(tokens, scope)) + '\n'


def get_lines(query, scopes):
    seen = set()
    for scope in scopes:
        # task: preserve whitespace from initial string - matters for punctuated sentences
        result = get_line(query, scope)
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
        if all(isinstance(t, Variable) or t.isdigit() for t in head):
            key = tuple(block[0])
            if body and len(body) == 1:
                db[key] = block[1:]
            elif key in db:
                return ''.join(get_line(statement, db) for statement in db[key])
            else:
                return 'Invalid key: ' + str(key) + '\n'
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
