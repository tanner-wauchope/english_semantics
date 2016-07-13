import collections
import itertools
import re


class Instance:
    def __init__(self, value=None):
        self.value = repr(self) if value is None else value

    def __eq__(self, other):
        return self.value == other.value


def tokenize(text):
    """
    :param str text: a text with at least one token
    :return list: a list of lists that contain the lexemes of each line
                  lexemes include indents, quotes, names, numbers, and punctuation
    """
    lines = [[]]
    for token in re.findall(r'[ \t]+|"(\\.|[^"])*"|[\w\.-]+|[:\n]', text):
        if token == '\n':
            lines.append([])
        elif not token[0] in ' \t' or not lines[-1]:
            lines[-1].append(token)
    return lines


def lex(lines):
    """
    :param list lines: a list of lists that contain the lexemes of each line
    :return list: a list of lists of non-indent lexemes for each line
    """
    if len(lines) == 0:
        return lines
    elif lines[0][0][0] in ' \t':
        raise IndentationError("Unexpected indent")
    elif len(lines) == 1:
        return lines

    precedent = ''
    blocks = []
    for line in lines:
        if line[0][0] not in ' \t':
            blocks.append([line])
        elif line[0].startswith(precedent):
            precedent = precedent or line[0]
            blocks[-1].append(line[len(precedent):])
        else:
            raise IndentationError('Inconsistent indent')

    result = []
    for block in blocks:
        result.append([])
        for tail in lex(block[1:]):
            result[-1].append(block[0] + [':'] + tail)
        else:
            result[-1].append(block[0])
    return result



def parse(items):
    for start in range(len(items)):
        grammar = items[start].grammar()
        for stop in range(len(items)):
            prefix, stem, suffix = items[:start], items[start:stop], items[stop:]
            for antecedent, consequent in grammar:
                if antecedent(stem):
                    return parse(prefix + consequent(stem) + suffix)

    if len(items) == 1:
        return items[0]

    for i, item in enumerate(items):
        vars(item)[i] = vars(item).get(i, [])
        vars(item)[i].append(items)


###############################

"""
a phrase is either an intention or an extension, which is an and-or tree of intentions
a noun phrase with no article gets an extension from scope or creates an intention in scope
a noun phrase with an indefinite article creates or overwrites an intention in scope
a noun phrase with a definite article gets an extension from scope or throws an error

a statement executed during read mode or that has one or more intentions executes in read mode
    if the statement is primitive (doesn't correspond with a method on the class of the first argument)
        union related facts from any extensions in the statement
        filter those facts by any intentions in the statement
            for each candidate at the position of an intention,
                verify that that the candidate or its class has all the right properties
                    if the intention's property is not directly matched,
                        evaluate any methods on the candidate class that unify with the property
                        try to match with any of the results
    otherwise, execute each line in a binding of the statement's definition

a statement executed during write mode that contains only extensions executes in write mode
    if the statement is primitive, the statement is linked to its constituents
    otherwise, execute each line in the statement's definition

a line that unifies with a definition should execute fully during recursive parsing
a line without a colon that does not fully unify is executed as a primitive read or write
a line with a colon is a definition

'get' accepts an intention and returns an extension containing any matching deterministic intentions
'make' accepts an intention and returns an extension containing one new deterministic extension
"""


class Instance:
    def __init__(self, value=None):
        self.value = repr(self) if value is None else value

    def __eq__(self, other):
        return self.value == other.value


def unifies(statement, signature):
    """ statement must be deterministic """
    if len(statement) != len(signature):
        return False
    for phrase, kind in zip(statement, signature):
        if not isinstance(phrase, type(kind)):
            return False
        for position in vars(kind):
            for constraint in vars(kind)[position]:
                query = list(constraint)
                query[position] = phrase
                if not read(query):
                    return False
    return True


def read(statement):
    for signature, definition in vars(type(statement[0])):
        if unifies(statement, signature):
            return definition(statement)

    facts = set()
    for i, phrase in enumerate(statement):
        for entity in phrase:
            if hasattr(entity, '__dict__'):
                for fact in vars(entity)[i]:
                    if unifies(fact, statement):
                        facts.add(fact)

    for i, phrase in enumerate(statement):
        if not phrase:
            statement = statement[:i] + (tuple(fact[i] for fact in facts),) + statement[i + 1:]


def write(statement):
    pass


def parse():
    pass

###############################

def predicate(parts, query=False):
    facts = set()
    for i, part in enumerate(parts):
        for entity in part:
            if hasattr(entity, '__dict__'):
                facts &= vars(entity)[i]

    matches = []
    for fact in facts:
        if unifies(fact, parts):
            matches.append(fact)

    for i, part in enumerate(parts):
        if not part:
            value = ()
            for match in matches:
                value += (match[i],)
            parts = parts[:i] + (value,) + parts[i + 1:]

    for fact in itertools.product(parts):
        for i, entity in enumerate(fact):
            if hasattr(entity, '__dict__'):
                entity[i] = entity.get(i, set())
                entity[i].add(fact)


def unifies(items, rule):
    if len(items) != len(rule):
        return False
    for item, kind in zip(items, rule):
        # TODO improve by looping over entities in item and entities in kind
        if not isinstance(item, type(kind)):
            return False
        elif hasattr(item, '__dict__') and hasattr(kind, '__dict__'):
            # TODO improve by handling derived properties
            for relation in vars(item).items():
                if relation not in vars(kind).items():
                    return False
        elif item != kind:
            return False
    return True


def parse(items, grammar):
    for item, start in enumerate(items):
        for function, rule in reversed(grammar):
            stop = start + len(rule)
            prefix, stem, suffix = items[:start], items[start:stop], items[stop:]
            if unifies(stem, rule):
                return parse(prefix + (function(stem),) + suffix, grammar)
    return items


def split(line, delimiters=' \t'):
    pattern = r'[^"' + delimiters + r']+|"(\\.|[^"])*"'
    return re.findall(pattern, line)


def evaluate(line, scope):
    """
    the colon is needed for function definitions, because length 1 signatures are possible
    all overloaded definitions have a length 1 signature?
    """
    scope['_grammar_'] = scope.get('_grammar_', collections.OrderedDict())
    segments = split(line, delimiters=":")
    if len(segments[0]):
        return
    lexemes = split(segments[0])
    if len(lexemes) == 0:
        raise SyntaxError("Leading colon")
    result = parse(lexemes, segments)
    assert len(result) > 0

    if len(segments) == 1:
        if len(result) == 1:
            return result[0]
        else:
            predicate(result)
            signature = [type(item) for item in result]
            scope['_grammar_'] = predicate, signature
    else:
        new_meaning = evaluate(segments[1:], scope)
        if result in scope:
            function = scope[result]
        else:
            def function(parts, query=False):
                for meaning in function.meanings:
                    meaning(parts, query=query)
            function.meanings = []
        function.append(new_meaning)
        scope['_grammar_'][function] = function, result