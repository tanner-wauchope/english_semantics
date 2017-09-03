import itertools
import sys


def lex(line):
    if not line:
        return []
    result = [[line[0]]]
    for char in line[1:]:
        token = result[-1]
        extend_alpha = token[0].isalpha() and char.isalpha()
        extend_digit = token[0].isdigit() and char.isdigit()
        if extend_alpha or extend_digit:
            token.append(char)
        else:
            result.append([char])
    return [''.join(token) for token in result]


class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name + str(id(self))


def tokenize(lexemes, variables):
    result = []
    new_variables = {}
    for lexeme in lexemes:
        if lexeme[0].isupper():
            if lexeme in variables:
                result.append(variables[lexeme])
            elif lexeme in new_variables:
                result.append(new_variables[lexeme])
            else:
                new_variables[lexeme] = Variable(lexeme)
                result.append(new_variables[lexeme])
        elif not lexeme.isspace():
            result.append(lexeme)
    return tuple(result), new_variables


def parse(block):
    results = []
    variables = {}
    for statement in block:
        lexemes, new_variables = tokenize(statement, variables)
        variables.update(new_variables)
        results.append(lexemes)
    return results[0], results[1:], variables


def guess_variable(consumer, consumed, scope):
    if isinstance(consumer[0], Variable):
        for i in range(1, len(consumed) + 1):
            if isinstance(consumed[i - 1], Variable):
                return
            proposal = {**scope, **{consumer[0]: consumed[:i]}}
            yield from unify(consumer[1:], consumed[i:], proposal)


def interpolate(pattern, scope):
    if not hasattr(pattern, '__iter__'):
        return scope.get(pattern, pattern)
    result = []
    for token in pattern:
        if token in scope:
            replacement = interpolate(scope[token], scope)
            if hasattr(replacement, '__iter__'):
                result.extend(replacement)
            else:
                result.append(replacement)
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


def conj(*goals):
    def goal(scope):
        result = goals[0](scope)
        for subgoal in goals[1:]:
            result = itertools.chain.from_iterable(map(subgoal, result))
        return result
    return goal


def disj(*goals):
    def goal(scope):
        subgoal_streams = (subgoal(scope) for subgoal in goals)
        return itertools.chain.from_iterable(subgoal_streams)
    return goal


def definition(conjuncts, db):
    goals = (search(conjunct, db) for conjunct in conjuncts)
    return conj(*goals)


def search(statement, db):
    def goal(scope):
        goals = []
        for key in db:
            if db[key] is True:
                goals.append(match(statement, key))
            else:
                head, body, _ = parse(db[key])
                goals.append(conj(match(head, statement), definition(body, db)))
        return disj(*goals)(scope)
    return goal


def get_line(tokens, scope):
    return ''.join(str(x) for x in interpolate(tokens, scope)) + '\n'


def get_lines(query, scopes):
    seen = set()
    for scope in scopes:
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
    if any(line for line in block):
        head, body, variables = parse(block)
        if all(isinstance(t, Variable) or t.isdigit() for t in head):
            key = tuple(item for item in block[0] if not item.isspace())
            if body and len(body) == 1:
                db[key] = body
            elif key in db:
                return ''.join(get_line(statement, db) for statement in db[key])
            else:
                return 'Invalid key: ' + str(key) + '\n'
        elif body:
            db[head] = block
        elif variables:
            query = search(head, db)
            stream =  list(itertools.islice(query({}), 1000))
            debug('Stream', stream)
            lines = get_lines(interpolate(block[0], variables), stream)
            return ''.join(lines) or "No results found.\n"
        else:
            db[head] = True
    return ''


def main(db=None):
    if db is None:
        db = {}
    print("Protolanguage (Version 0)")
    while True:
        lines = [lex(input('>>> '))]
        if any(token[0].isupper() for token in lines[0]):
            while lines[-1]:
                lines.append(tuple(lex(input('...     '))))
            lines.pop()
        print(run(lines, db), end='')
        debug('DB', db.items())


if __name__ == '__main__':
    main()
