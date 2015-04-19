def quoted(text):
    """
    :param text: text that might start and end with quotation marks
    :return: whether the text starts and ends with quotation marks
    """
    return text != '"' and text.startswith('"') and text.endswith('"')


def quote_split(text):
    """
    :param text: text with an even number of quotation marks
    :return: sequence of texts with the quoted sections separated
    """
    lexemes = ['']
    for character in text:
        if character != ' ' or lexemes[-1].startswith('"'):
            lexemes[-1] += character
        if not lexemes[-1].endswith(character) or quoted(lexemes[-1]):
            lexemes.append('')
    return lexemes


def suffix_split(text, suffix):
    """
    :param text: text to be split into segments
    :param suffix: text that ends each segment
    :return: non-whitespace segments with each suffix preserved
    """
    segments = text.split(suffix)
    segments = (segment for segment in segments if not segment.isspace())
    return (segment + suffix for segment in segments)


def scan(text):
    """
    :param text: a block of english text
    :param delimiters: a sequence of delimiters for splitting the text
    :return: a lexeme tree that is ready to be cast into types
    """
    segments = suffix_split(text, '.\n')
    segments = (suffix_split(segment, '\n\t') for segment in segments)
    return (quote_split(segment) for segment in segments)

