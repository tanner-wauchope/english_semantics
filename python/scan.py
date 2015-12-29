import shlex


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


class InvalidClause(SyntaxError):
    """
    Raised when a line starts with a quote or has unclosed quotes.
    """
    pass


class InvalidToken(SyntaxError):
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
    Checks that the sentence contains more lines than clauses.
    :param sentence: a sentence that may be spread across multiple lines
    """
    if len(split(sentence, '\n')) is len(split(sentence, ',\n\t')):
        return sentence.strip()
    else:
        raise InvalidSentence('Contains more lines than clauses')


def validate_clause(clause):
    """
    Checks if the line starts with a quote or has unclosed quotes.
    :param clause: text that may contain possessives or embedded quotes
    """
    if clause.startswith('"'):
        raise InvalidClause('Clause starts with a quote')
    elif clause.count('"') % 2 == 1:
        raise InvalidClause('Clause missing quotation mark')
    else:
        return clause.strip()


def split(text, delimiter):
    segments = text.split(delimiter)
    if segments and not segments[-1].strip():
        segments = segments[:-1]
    return segments


def is_quote(lexeme):
    if len(lexeme) < 2 or lexeme[-1] != '"':
        return False

    trailing_slashes = 0
    for char in reversed(lexeme[:-1]):
        if char == '\\':
            trailing_slashes += 1
        else:
            break
    return trailing_slashes % 2 == 0


def lexemes(clause):
    """
    :param clause: text that may contain possessives or embedded quotes
    :return: a list of lexemes, which are words or quotes
    """
    lexemes = []
    lexeme = []
    for char in clause:
        if char not in " '" or lexeme[:1] == ['"']:
            lexeme.append(char)
        if lexeme[:1] != ['"'] and char in " '" or is_quote(lexeme):
            lexeme = []
        if char == "'":
            lexeme.append(char)
        if lexeme and [lexeme] != lexemes[-1:]:
            lexemes.append(lexeme)
    return [''.join(token) for token in lexemes]


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
            clause = validate_clause(clause)
            sentences[-1].append(lexemes(clause))
    return sentences
