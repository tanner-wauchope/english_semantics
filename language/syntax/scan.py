from language.syntax.primitives import quote


def quote_split(text):
    """
    :param text: text with an even number of quotation marks
    :return: sequence of texts with the quoted sections separated
    """
    lexemes = ['']
    for character in text:
        is_word = lexemes[-1].startswith('"')
        if character != ' ' or not is_word:
            lexemes[-1] += character
        if character == ' ' and is_word or quote.match(lexemes[-1]):
            lexemes.append('')
    return lexemes


def punctuation_split(text, delimiter):
    """
    :param text: text to be split into segments
    :param delimiter: text that ends each segment
    :return: non-whitespace segments
    """
    result = []
    for segment in text.split(delimiter):
        if not segment.isspace():
            result.append(segment)
    return result


def scan(block):
    """
    :param block: a text paragraph
    :return: sentences that contain lines that contain lexemes
    """
    sentences = []
    for sentence in punctuation_split(block, '.\n'):
        sentences.append([])
        for line in punctuation_split(sentence, ',\n\t'):
            sentences[-1].append([])
            for lexeme in quote_split(line):
                sentences[-1][-1].append((lexeme))
    return sentences
