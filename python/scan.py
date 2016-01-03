import string


class InvalidParagraph(SyntaxError):
    """
    Raised when a paragraph does not end with a period.
    """
    pass


class InvalidSentence(SyntaxError):
    """
    Raised when a paragraph contains more lines the clauses.
    """
    pass


def validate_paragraph(paragraph):
    """
    Checks if the paragraph ends with a period.
    :param paragraph: text that may contain possessives or embedded quotes
    """
    if paragraph.strip().endswith('.'):
        return paragraph.strip()
    else:
        raise InvalidParagraph('A paragraph should end with a period')


def validate_sentence(sentence):
    """
    Checks that the sentence doesn't split clauses into multiple lines.
    :param sentence: a sentence that may be spread across multiple lines
    """
    if len(sentence.split('\n')) is len(sentence.split(',\n\t')):
        return sentence.strip()
    else:
        raise InvalidSentence('Contains more lines than clauses')


def complete(text):
    phrase = text.lstrip()
    if not phrase or phrase[0] not in '"(':
        return True

    quote = (
        phrase[0] == '"' and
        phrase[-1] == '"' and
        (len(phrase) - len(phrase.strip('\\'))) % 2 == 0
    )
    parenthetical = (
        phrase[0] == '(' and
        phrase[-1] == ')' and
        phrase.count('(') == phrase.count(')')
    )
    return quote or parenthetical


def lexemes(clause) -> list:
    """
    :param str clause: one line of english text
    :return: basic tokens, quotes, and parentheticals
    """
    clause = clause.strip(':\n') + '\n'
    results = []
    lexeme = ''
    for char in clause:
        if char in string.whitespace + "'" and complete(lexeme):
            results.append(lexeme.strip())
            lexeme = ''
        lexeme += char
    return [result for result in results if result]


def scan(paragraph):
    """
    :param paragraph: text without empty lines or invisible whitespace
    :return: sentences that contain lines that contain lexemes
    """
    paragraph = validate_paragraph(paragraph)
    sentences = []
    for sentence in paragraph[:-1].split('.\n'):
        sentence = validate_sentence(sentence)
        sentences.append([])
        for clause in sentence.split(',\n\t'):
            clause = clause.strip()
            sentences[-1].append(lexemes(clause))
    return sentences
