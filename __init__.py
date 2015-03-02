from lexer import tokenize

package_name = 'English Semantics 0.1'

def parse_line(line):
    tokens = tokenize(line)
    result = tokens.pop(0)
    while tokens:
        result = result.combine(tokens.pop(0))
    return repr(result)

def parse_block(block):
    return '\n'.join(parse_line(line) for line in block)


