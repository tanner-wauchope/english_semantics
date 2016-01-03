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


def validate_paragraph(paragraph) -> str:
    """
    Checks if the paragraph ends with a period.
    :param str paragraph: text that may contain possessives or embedded quotes
    """
    if paragraph.strip().endswith('.'):
        return paragraph.strip()
    else:
        raise InvalidParagraph('A paragraph should end with a period')


def validate_sentence(sentence) -> str:
    """
    Checks that the sentence doesn't split clauses into multiple lines.
    :param str sentence: a sentence that may be spread across multiple lines
    """
    if len(sentence.split('\n')) is len(sentence.split(',\n\t')):
        return sentence.strip()
    else:
        raise InvalidSentence('Contains more lines than clauses')


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
    paragraph = validate_paragraph(paragraph)
    sentences = []
    for sentence in paragraph[:-1].split('.\n'):
        sentence = validate_sentence(sentence)
        sentences.append([])
        for clause in sentence.split(',\n\t'):
            sentences[-1].append(lexemes(clause))
    return sentences
