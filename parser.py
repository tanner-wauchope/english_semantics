

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
    >>> combine(parts_of_speech.cast(message))
    User_(the_).leave_(should_, in_=Seconds_(12))
    >>> message = "the user is active. the user is not banned")
    >>> combine(parts_of_speech.cast(message))
    User_(the_).is_(active_)
    User_(the_).is_(banned_(not_))
    >>> message = "if the user is active, the user is not banned"
    >>> combine(parts_of_speech.cast(message))
    if User_(the_).is_(active_):
        User_(the_).is_(banned_(not_))
    """
    if len(symbols) == 0:
        return ''
    elif len(symbols) == 1:
        return symbols[0]
    return parse(simplify(symbols))

class Parser:
    def __init__(self, buffer=[]):
        self._buffer = buffer

    def __next__(self):
        block_ending = self.block_ending()
        if block_ending:
            block = '\n'.join(self.buffer[:block_ending])
            self.buffer = self.buffer[block_ending:]
            return repr(parse(block))
        raise StopIteration

    def block_ending(self):
        for i, line in enumerate(self.buffer):
            if not line.strip():
                return i

    def read(self, line):
        self.buffer.append(line)
