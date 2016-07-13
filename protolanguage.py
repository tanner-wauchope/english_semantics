# list indexing and dict indexing should probably only affect nouns (capitalized tokens)


def add_block(quote, statement, program):
    joined_quote = '\n'.join(quote)
    if joined_quote and not joined_quote.isspace():
        if statement:
            statement.append(parse(quote))
        else:
            statement.append(quote)
    if statement:
        program.append(statement)


def parse(lines):
    quote = []
    statement = []
    program = []
    for line in lines:
        if line.startswith(' '):
            raise IndentationError("Indentation can only contains tabs.")
        elif line.isspace() or line == '':
            quote.append(line[1:])
        elif line.startswith('\t'):
            quote.append(line[1:])
        else:
            add_block(quote, statement, program)
            quote = []
            statement = line.split()
    add_block(quote, statement, program)
    return program


def lookup(arguments, scope, times_run=[]):
    """
    The outer scope is stored at position 0
    """
    print('lookup ' + str(len(times_run)))
    print(arguments)
    print(scope)
    print()
    times_run.append(1)
    if len(times_run) > 20:
        assert False
    assert arguments, "Tried to lookup an empty pattern"
    if scope is None:
        return None
    for lexical_scope, definition in reversed(scope[1:]):
        unifies = (
            len(definition) - 1 == len(arguments) and (
                len(arguments) == 1 and definition[0] == arguments[0] or
                all(k == v or k.isupper() for k, v in zip(definition[:-1], arguments))
            )
        )
        if unifies:
            return lexical_scope, definition
    return lookup(arguments, scope[0])


def evaluate(statement, scope, times_run=[]):
    print('evaluate')
    print(statement)
    print(scope)
    print()

    # the base case is an indented block with no head
    if len(statement) == 1 and isinstance(statement[0], list):
        return statement[0]

    # otherwise try to lookup a definition for the statement
    scope_and_definition = lookup(statement, scope)
    if scope_and_definition:
        lexical_scope, definition = scope_and_definition
        # execute the identified definition
        signature, body = definition[:-1], definition[-1]
        slots = [(i, slot) for (i, slot) in enumerate(signature) if slot.isupper()]
        local_scope = [lexical_scope]
        for i, slot in slots:
            if isinstance(statement[i], str) and statement[i].isupper():
                arg_scope_and_definition = lookup(statement[i], local_scope)
                if arg_scope_and_definition:
                    value = arg_scope_and_definition[1][-1]
                else:
                    value = None
            else:
                value = statement[i]
            if value:
                local_scope.append((local_scope, [slot, value])) # maybe wrap the body?
        result = []
        for consequence in parse(body):
            result += evaluate(consequence, local_scope)
        # move uppercase variables into the calling scope
        for i, arg in slots:
            _, final_definition = lookup([arg], local_scope)
            scope.append((scope, final_definition))
        return result
    elif statement and isinstance(statement[-1], list):
        # create a definition
        scope.append((scope, statement))
    else:
        raise SyntaxError("No statement matching pattern: " + str(statement[:-1]))
