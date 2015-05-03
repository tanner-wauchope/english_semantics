

def phrase_split(phrase):
    """
    :param phrase: text lacking quotes but possibly having possessives
    :return: a list of words and possibly clitics
    """
    lexemes = []
    for lexeme in phrase.split(' '):
        try:
            noun, clitic = lexeme.split("'")
            lexemes.append(noun)
            lexemes.append("'" + clitic)
        except ValueError:
            lexemes.append(lexeme)
    return lexemes


def lexemes(line):
    """
    :param text: text that may contain possessives or embedded quotes
    :return: a list of lexemes, which are words, clitics, or quotes
    """
    lexemes = []
    for i, segment in enumerate(line.split('"')):
        if i % 2 == 0:
            lexemes.extend(phrase_split(segment))
        else:
            lexemes.append('"' + segment + '"')
    return lexemes


def scan(paragraph):
    """
    :param paragraph: a text whose lines do not have trailing whitespace
    :return: sentences that contain lines that contain lexemes
    """
    sentences = []
    for sentence in paragraph.split('.\n')[:-1]:
        sentences.append([])
        for line in sentence.split(',\n\t'):
            sentences[-1].append(lexemes(line))
    return sentences
