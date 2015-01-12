import re

import parts_of_speech

def combine(parts):
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
    while parts:
        for i in range(len(parts) - 2):
            try:
                combination = parts(i).combine(parts(i + 1))
                del parts[i:i + 2]
                parts.insert(i, combination)
                break
            except ValueError:
                pass
    return parts[0]

def parse_paragraph(block):
    statements = []
    for sentence in re.split(r'\.[ \t]*[\n\r\f]+', block):
        python = repr(combine(parts_of_speech.cast(sentence)))
        statements.append(python)
    return '\n'.join(statements)

def parse_line(line, lines=[]):
    lines.append(line)
    if not line.strip():
        block = '\n'.join(lines)
        lines = []
        return parse_paragraph(block)