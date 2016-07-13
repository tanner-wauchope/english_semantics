import pprint
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


def families_at_outer_level(phrases) -> list:
    """
    :param list phrases: phrases with indentation >= the first phrase
    :return: Families of lines rooted at the first phrase's level.
    """
    level = phrases[0].level
    result = []
    for phrase in phrases:
        if phrase.level == level:
            result.append([phrase])
        elif phrase.level > level:
            result[-1].append(phrase)
        else:
            message = 'unindent does not match outer indentation level'
            raise IndentationError(message)
    return result


def indentation_hierarchy(phrases) -> grammar.Tree:
    """
    :param list phrases: lines with varying indentation
    :return: a single tree mirroring the structure of the indented lines
    """
    assert len(phrases) > 0
    parents = []
    for family in families_at_outer_level(phrases):
        parent, children = family[0], family[1:]
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


def lex(text) -> grammar.Tree:
    """
    :param text: an English text
    :return: a single tree representing all of the text
    """
    phrases = []
    unit = None
    for line in split(text, delimiters='\n'):
        if not line.isspace():
            level, unit = indentation(line, unit)
            tokens = tokenize(line)
            phrase = parse(tokens)
            phrases.append(phrase)
    return indentation_hierarchy(phrases)

# Parser

class ParsingError(SyntaxError):
    """
    Thrown when two phrases cannot be merged.
    The first phrase cannot specify the second,
    and the second phrase cannot complement the first.
    """
    pass


def first(tree):
    """
    :param tree: a binary tree of constituencies
    :return: the left-most node in the tree
    """
    if not tree.specifier:
        return tree
    return first(tree.specifier)


def last(tree):
    """
    :param tree: a binary tree of constituencies
    :return: the right-most node in the tree
    """
    if not tree.complement:
        return tree
    return last(tree.complement)


def contains(word_classes, word):
    """
    :param word_class: a set of word classes
    :param word: a word that could be an instance of the word classes
    :return: whether the word is an instance of any of the word classes
    """
    for word_class in word_classes:
        if isinstance(word, word_class):
            return True


def merge(tree, other):
    """
    Minimal attachment takes precedence over late closure.
    :param tree: a binary-branching dependency tree of words
    :param other: a binary-branching dependency tree of words
    :return: one of the trees, except with the other tree added as a subtree
    """
    if contains(last(tree).COMPLEMENTED_BY, other):
        last(tree).complement = other
        return tree
    elif contains(tree.SPECIFIES, first(other)):
        first(other).specifier = tree
        return other
    elif contains(other.COMPLEMENTS, last(tree)):
        last(tree).complement = other
        return tree
    elif contains(first(other).SPECIFIED_BY, tree):
        first(other).specifier = tree
        return other
    raise ParsingError('Phrases cannot merge: ' + str([tree, other]))


def garden_path(tokens):
    """
    :param tokens: a list of tokens
    :return: a list of python trees
    """
    trees = tokens[:1]
    for token in tokens[1:]:
        try:
            trees[-1] = merge(trees[-1], token)
        except ParsingError:
            try:
                trees = garden_path(trees)
                trees[-1] = merge(trees[-1], token)
            except ParsingError:
                trees.append(token)
    if len(tokens) == len(trees):
        return trees
    else:
        return garden_path(trees)


def parse(tokens):
    """
    :param block: sentences that contain lines that contain tokens
    :return: a list of lists of binary trees that represent sentences
    """
    new = garden_path(tokens)
    if len(new) == 1:
        return new[0]
    else:
        raise ParsingError('Phrases cannot merge: ' + str(new))


# Experimental parser changes


def initialize_chart(tokens):
    total = len(tokens)
    chart = []
    for i in range(total):
        chart.append([])
        for j in range(total):
            chart[i].append([])
            cell = chart[i][j]
            if j == i:
                cell.append(tokens[i])
            elif j < i:
                cell.append(None)
    return chart


def is_dependent(tree, other):
    """
    Minimal attachment takes precedence over late closure.
    :param tree: a binary-branching dependency tree of words
    :param other: a binary-branching dependency tree of words
    :return: whether tree can merge with other
    """
    return (
        contains(last(tree).COMPLEMENTED_BY, other) or
        contains(tree.SPECIFIES, first(other)) or
        contains(other.COMPLEMENTS, last(tree)) or
        contains(first(other).SPECIFIED_BY, tree)
    )


def merges(trees, others) -> list:
    for tree in trees:
        for other in others:
            if is_dependent(tree, other):
                return True


def build_chart(tokens) -> list:
    """Alternative parser implementation based on CYK algorithm"""
    chart = initialize_chart(tokens)
    for stop in range(len(tokens)):
        for start in reversed(range(stop + 1)):
            for k in range(start, stop + 1):
                head = [tokens[k]]
                left = start == k or merges(chart[start][k - 1], head)
                right = k == stop or merges(head, chart[k + 1][stop])
                if left and right and head[0] not in chart[start][stop]:
                    chart[start][stop].extend(head)
    return chart


def trace(chart, i, j) -> grammar.Tree:
    heads = chart[i][j]
    if len(heads) > 1:
        pprint.pprint(chart)
        print(i)
        print(j)
        for head in heads:
            print(head.head)
        raise ParsingError('Global ambiguity: ' + str(heads))

    head = heads[0]
    if head is None:
        return head

    if head.index > i:
        head.specifier = trace(chart, i, head.index - 1)
    if head.index < j:
        head.complement = trace(chart, head.index + 1, j)
    return head


def parse(tokens) -> grammar.Tree:
    for i, token in enumerate(tokens):
        token.index = i
    chart = build_chart(tokens)
    if len(chart[0][len(tokens) - 1]) == 0:
        pprint.pprint(chart)
        raise ParsingError('No valid parse: ' + str(tokens))
    return trace(chart, 0, len(tokens) - 1)