
def split(text, delimiter):
    segments = text.split(delimiter)
    if segments and segments[0].isspace():
        segments = segments[1:]
    if segments and segments[-1].isspace():
        segments = segments[:-1]
    return segments


def validate_phrase(phrase):
    pass


def words(phrase):
    """
    :param phrase: text lacking quotes but possibly having possessives
    :return: a list of words, including clitics
    """
    lexemes = []
    for lexeme in split(phrase, ' '):
        try:
            noun, clitic = lexeme.split("'")
            lexemes.append(noun)
            lexemes.append("'" + clitic)
        except ValueError:
            lexemes.append(lexeme)
    return lexemes

def validate_line(line):
    """
    Checks if the line starts with a quote or has an odd number of quotes.
    :param line: text that may contain possessives or embedded quotes
    """
    if line.startswith('"'):
        raise SyntaxError('Lines should not start with a double-quote')
    elif line.count('"') % 2 == 1:
        raise SyntaxError('Lines should not an odd number of double-quotes')


def lexemes(line):
    """
    :param line: text that may contain possessives or embedded quotes
    :return: a list of lexemes, which are words or quotes
    """
    validate_line(line)
    lexemes = []
    for i, segment in enumerate(split(line, '"')):
        if i % 2 == 0:
            lexemes.extend(words(segment))
        else:
            lexemes.append('"' + segment + '"')
    return lexemes


def validate_sentence(sentence):
    number_of_lines = len(split(sentence, '\n'))
    number_of_phrases = len(split(sentence, ',\n\t'))
    if number_of_lines is not number_of_phrases:
        raise SyntaxError('Number of lines is not number of phrases')


def scan(paragraph):
    """
    :param paragraph: a text whose lines do not have trailing whitespace
    :return: sentences that contain lines that contain lexemes
    """
    sentences = []
    for sentence in split(paragraph, '.\n'):
        sentences.append([])
        for line in sentence.split(',\n\t'):
            sentences[-1].append(lexemes(line))
    return sentences
