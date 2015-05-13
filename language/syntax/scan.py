
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


def validate_paragraph(paragraph):
    """
    Checks if the paragraph ends with a period.
    :param paragraph: text that may contain possessives or embedded quotes
    """
    if not paragraph.endswith('.\n'):
        raise InvalidParagraph('A paragraph should end with a period')


def validate_sentence(sentence):
    """
    Checks that the sentence contains more lines that clauses.
    :param sentence: a sentence that may be spread across multiple lines
    """
    if len(split(sentence, '\n')) is not len(split(sentence, ',\n\t')):
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


def split(text, delimiter):
    segments = text.split(delimiter)
    if segments and not segments[-1].strip():
        segments = segments[:-1]
    return segments


def words(phrase):
    """
    :param phrase: text lacking quotes but possibly having possessives
    :return: a list of words and clitics
    """
    result = []
    for lexeme in split(phrase, ' '):
        if "'" in lexeme and not lexeme[0] == "'" and not lexeme[-1] == "'":
            parts = lexeme.split("'")
            result.append(parts[0])
            result.append("'" + parts[1])
        else:
            result.append(lexeme)
    return result


def lexemes(clause):
    """
    :param clause: text that may contain possessives or embedded quotes
    :return: a list of lexemes, which are words or quotes
    """
    result = []
    for i, segment in enumerate(split(clause, '"')):
        if i % 2 == 0:
            result.extend(words(segment))
        else:
            result.append('"' + segment + '"')
    return result


def scan(paragraph):
    """
    :param paragraph: text without empty lines or invisible whitespace
    :return: sentences that contain lines that contain lexemes
    """
    validate_paragraph(paragraph)
    sentences = []
    for sentence in split(paragraph, '.\n'):
        validate_sentence(sentence)
        sentences.append([])
        for clause in sentence.split(',\n\t'):
            validate_clause(clause)
            sentences[-1].append(lexemes(clause))
    return sentences
