from . import Lexer

def simplify(symbols):
    for i, (current, next) in enumerate(zip(symbols, symbols[1:])):
        combination = current.combine(next)
        if combination:
            symbols[i:i + 1] = [combination]
            return symbols
    raise SyntaxError("Symbols cannot be simplified: " + str(symbols))

def parse(symbols):
    """
    :param parts: a list of objects representing words
    :return: an object representing a sentence
    >>> message = "the user should leave in 12 seconds"
    >>> combine(words.cast(message))
    the(User).should(leave, in_=quantifier(12)(Seconds))
    >>> message = "if the user is active, the user is not banned"
    >>> combine(words.cast(message))
    if the(User).is_(active):
        the(User).is_(not_(banned))
    """
    if len(symbols) == 0:
        return ''
    elif len(symbols) == 1:
        return symbols[0]
    return parse(simplify(symbols))

class Parser:
    def __init__(self, buffer=[]):
        self._buffer = buffer
        self.lexer = Lexer()

    def __next__(self):
        block_ending = self.block_ending()
        if block_ending:
            block_lines = self.buffer[:block_ending]
            self.buffer = self.buffer[block_ending:]
            self.lexer.read('\n'.join(block_lines))
            return repr(parse(self.lexer.flush()))
        raise StopIteration

    def block_ending(self):
        for i, line in enumerate(self.buffer):
            if not line.strip():
                return i

    def read(self, line):
        self.buffer.append(line)
