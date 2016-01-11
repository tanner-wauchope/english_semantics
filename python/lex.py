import re

from plain_english.python import grammar


def split(text, delimiters=' \t\n') -> list:
    """
    :param text: text that may contain the delimiters or quotes
    :param delimiters: tokens to be omitted if unquoted
    :return: the text split by unquoted delimiters
    """
    text += delimiters
    result = []
    segment = []
    state = 'unquoted'
    for char in text:
        if state == 'unquoted' and char == '"':
            state = 'quoted'
            segment.append(char)
            continue
        elif state == 'quoted' and char == '"':
            state = 'unquoted'
            segment.append(char)
            continue
        elif state == 'quoted' and char == '\\':
            state = 'escaped'
            continue
        elif state == 'escaped':
            state = 'quoted'
            segment.append(char)
            continue

        if not(char in delimiters and state == 'unquoted'):
            segment.append(char)
        elif segment:
            result.append(''.join(segment))
            segment = []

    if state == 'quoted':
        raise SyntaxError('Unclosed quotation: ' + ''.join(segment))
    return result


def indentation(line, unit) -> tuple:
    level = grammar.count_prefix(' \t', line)
    units = set(line[:level])
    if len(units) > 1 or unit and unit not in units:
        message = 'Indentation must not mix tabs and spaces.'
        raise IndentationError(message)
    elif not unit and len(units) == 1:
        unit = units.pop()
    return level, unit


def classify(lexeme) -> type:
    """
    :param str lexeme: a lexeme that is possibly punctuated or numeric
    :return: an instance of the word class of the lexeme
    """
    for word_class in grammar.categories:
        if lexeme.lower() in word_class.KEYWORDS:
            return word_class(lexeme)
    for word_class in grammar.categories:
        pattern = word_class.PATTERN
        if pattern and re.match(pattern + '$', lexeme):
            return word_class(lexeme)
    raise SyntaxError('Invalid English token: ' + lexeme)


def tokenize(line) -> list:
    """
    :param str line: one logical line of english text (maybe a block quote)
    :return: basic tokens, quotes, and parentheticals
    """
    tokens = []
    line = ('_' + line).strip(':., \t\n')[1:] + '\n'
    for segment in split(line):
        if grammar.Quote.valid(segment):
            tokens.append(grammar.Quote(segment))
        else:
            index = segment.find("'")
            if index == -1:
                tokens.append(classify(segment))
            else:
                stem, suffix = segment[:index], segment[index:]
                tokens.append(classify(stem))
                tokens.append(classify(suffix))
    return tokens


#
# def non_destructive_split(text, delimiters):
#     result = []
#     for char in text:
#         if char in delimiters or not result or result[-1][-1] in delimiters:
#             result.append([char])
#         else:
#             result[-1].append(char)
#     return [''.join(segment) for segment in result]
#
#
# def nest(sequence, opener, closer):
#     stack = [[]]
#     for piece in non_destructive_split(sequence, opener + closer):
#         if piece in opener:
#             stack.append([])
#         elif piece in closer:
#             assert len(stack) > 1, 'Unopened delimiter'
#             stack[-2].append(stack.pop())
#         else:
#             stack[-1].append(piece)
#     assert len(stack) == 1, 'Unclosed delimiter'
#     return stack.pop()


def conjuncts(phrases) -> list:
    result = []
    for phrase in phrases:
        level = phrases[0].level
        if phrase.level == level:
            result.append([phrase])
        elif phrase.level > level:
            result[-1].append(phrase)
        else:
            message = 'unindent does not match outer indentation level'
            raise IndentationError(message)
    return result


def indentation_hierarchy(phrases) -> grammar.Tree:
    assert len(phrases) > 0
    parents = []
    for conjunct in conjuncts(phrases):
        parent, children = conjunct[0], conjunct[1:]
        if children:
            complement = indentation_hierarchy(children)
            parent.complement.append(complement)
        parents.append(parent)

    if len(parents) == 1:
        return parents[0]
    else:
        return grammar.And(
            'and',
            specifier=parents[:-1],
            complement=parents[-1:],
        )


#
# def deindent(stack, current_level) -> None:
#     while current_level != stack[-1].level:
#         phrase = stack.pop()
#         top = stack[-1]
#         top.complement.append(phrase)
#
#
# def indentation_hierarchy(phrases) -> list:
#     stack = [grammar.Tree('', level=0)]
#     for phrase in phrases:
#         top = stack[-1]
#         if phrase.level > top.level:
#             new = grammar.And('and', complement=[phrase], level=phrase.level)
#             stack.append(new)
#         elif phrase.level == top.level:
#             top.complement.append(phrase)
#         else:
#             deindent(stack, phrase.level)
#             top.complement.append(phrase)
#     deindent(stack, 0)
#     assert len(stack) == 1
#     return stack.pop()


def lex(text):
    phrases = []
    unit = None
    for line in split(text, delimiters='\n'):
        if not line.isspace():
            level, unit = indentation(line, unit)
            tokens = tokenize(line)
            phrase = grammar.Tree('', specifier=tokens, level=level)
            phrases.append(phrase)
    return indentation_hierarchy(phrases)
