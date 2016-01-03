import string


def closed(text) -> bool:
    """
    :param str text: text that may have an unclosed delimiter
    :return: whether the text has an unclosed delimiter
    """
    is_quote = (
        text[0] == '"' and
        text[-1] == '"' and
        (len(text) - len(text.strip('\\'))) % 2 == 0
    )
    is_parenthetical = (
        text[0] == '(' and
        text[-1] == ')' and
        text.count('(') == text.count(')')
    )
    return is_quote or is_parenthetical


def lexemes(clause) -> list:
    """
    :param str clause: one line of english text
    :return: basic tokens, quotes, and parentheticals
    """
    clause = clause.strip().strip(':') + '\n'
    must_capture = string.whitespace + "'"
    results = []
    lexeme = ''
    for char in clause:
        lexeme = lexeme.lstrip()
        unopened = not lexeme or lexeme[0] not in '"('
        if char in must_capture and (unopened or closed(lexeme)):
            results.append(lexeme.strip())
            lexeme = ''
        lexeme += char
    return [result for result in results if result]


def scan(paragraph) -> list:
    """
    :param str paragraph: text without empty lines or invisible whitespace
    :return: sentences that contain lines that contain lexemes
    """
    sentences = []
    for sentence in ('#' + paragraph).strip('. \n\t')[1:].split('.\n\t'):
        sentences.append([])
        for clause in sentence.strip().split(',\n\t'):
            sentences[-1].append(lexemes(clause))
    return sentences
