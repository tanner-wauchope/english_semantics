import pytest

from plain_english.python import grammar
from plain_english.python.lex import (
    split,
    indentation,
    classify,
    tokenize,
    conjuncts,
    indentation_hierarchy,
    lex,
)


# def test_non_destructive_split():
#     actual = non_destructive_split('\0\1abc\0\1def\0\1', '\0\1')
#     assert actual == ['\0', '\1', 'abc', '\0', '\1', 'def', '\0', '\1']


# def test_nest():
#     assert nest("abc", '(', ')') == ['abc']
#     assert nest("a(bc)d", '(', ')') == ['a', ['bc'], 'd']
#     assert nest("a(bc(d))", '(', ')') == ['a', ['bc', ['d']]]
#     assert nest('a(b)c(d)', '(', ')') == ['a', ['b'], 'c', ['d']]
#     assert nest('a(b(c)d(e))', '(', ')') == ['a', ['b', ['c'], 'd', ['e']]]


def test_split():
    # single lexemes
    assert split('"\n"', '\n') == ['"\n"']
    assert split('ab', '\n') == ['ab']

    # delimiter as prefix or suffix
    assert split('\n"\n"', '\n') == ['"\n"']
    assert split('"\n"\n', '\n') == ['"\n"']
    assert split('\nab', '\n') == ['ab']
    assert split('ab\n', '\n') == ['ab']

    # split quote and non-quote lexemes
    assert split('ab\ncd', '\n') == ['ab', 'cd']
    assert split('"\n"\n"\n"', '\n') == ['"\n"', '"\n"']
    assert split('ab\n"\n"', '\n') == ['ab', '"\n"']
    assert split('"\n"\nab', '\n') == ['"\n"', 'ab']

    # handle multiple occurrences of the delimiter
    assert split('ab\n\ncd', '\n') == ['ab', 'cd']

    # handle multiple delimiters
    assert split('ab \n cd', '\n ') == ['ab', 'cd']

    # split a quotation ending with an escaped backslash
    assert split(r'"\\"', '\n') == [r'"\"']

    # split string that whose ending quote is escaped
    with pytest.raises(SyntaxError):
        split('"\\"', '\n')


def test_indentation():
    # no prior indentation unit
    assert indentation('  ', None) == (2, ' ')
    assert indentation('\t\t', None) == (2, '\t')

    # same as prior indentation unit
    assert indentation('  ', ' ') == (2, ' ')
    assert indentation('\t\t', '\t') == (2, '\t')

    # first indentation contains spaces and tabs
    with pytest.raises(IndentationError):
        indentation(' \t', None)

    # indentation switches from tabs to spaces
    with pytest.raises(IndentationError):
        indentation(' ', '\t')

    # indentation switches from spaces to tabs
    with pytest.raises(IndentationError):
        indentation('\t', ' ')


def test_classify_valid():
    # closed word classes
    assert type(classify("'")) == grammar.Clitic
    assert type(classify('that')) == grammar.Complementizer
    assert type(classify('or')) == grammar.Or
    assert type(classify('a')) == grammar.Determiner
    assert type(classify('if')) == grammar.Subordinator

    # primitives
    assert type(classify('7')) == grammar.Number
    assert type(classify('"abc"')) == grammar.Quote

    # open word classes
    assert type(classify('it')) == grammar.Noun
    assert type(classify('has')) == grammar.Verb
    assert type(classify('Apple')) == grammar.Noun
    assert type(classify('make')) == grammar.Verb


def test_classify_invalid():
    # invalid quotation
    with pytest.raises(SyntaxError):
        classify('"abc"abc')

    # invalid number
    with pytest.raises(SyntaxError):
        classify("123.123.123")

    # invalid clitic
    with pytest.raises(SyntaxError):
        classify("'abc'abc")

    # empty token
    with pytest.raises(SyntaxError):
        classify('')


def test_tokenize():
    # lines with end punctuation
    tests = ['ab:', 'ab,', 'ab.']
    outputs = [['ab'], ['ab'], ['ab']]

    # lines with clitics
    tests.extend(["ab'", "ab's"])
    outputs.extend([['ab', "'"], ['ab', "'s"]])

    # line with whitespace and a quotation
    tests.append(' \t\nab "\t \n" cd\n\t ')
    outputs.append(['ab', '"\t \n"', 'cd'])

    # compare actual outputs on tests to expected outputs
    for test, output in zip(tests, outputs):
        actual = [actual.head for actual in tokenize(test)]
        assert actual == output


def test_conjuncts():
    # test level 0 with children at multiple levels
    phrases = [
        grammar.Tree('A:', level=0),
        grammar.Tree('B:', level=1),
        grammar.Tree('C', level=2),
        grammar.Tree('A:', level=0),
        grammar.Tree('B:', level=1),
        grammar.Tree('C', level=2),
    ]
    assert conjuncts(phrases) == [phrases[:3], phrases[3:]]

    # verify that a deindent past the current level causes an error
    with pytest.raises(IndentationError):
        conjuncts(phrases[2:4])


def test_indentation_hierarchy():
    phrases = [
        grammar.Tree('A:', level=0),
        grammar.Tree('B:', level=1),
        grammar.Tree('C', level=2),
        grammar.Tree('C', level=2),
        grammar.Tree('A:', level=0),
        grammar.Tree('B:', level=1),
        grammar.Tree('C', level=2),
        grammar.Tree('C', level=2),
    ]
    # a single line should just be returned
    assert indentation_hierarchy([phrases[0]]) == phrases[0]

    # check for a conjunction with the proper recursive structure
    result = indentation_hierarchy(phrases)
    assert isinstance(result, grammar.And)
    assert str(result) == 'A: B: C and C and A: B: C and C'


# def test_lex():
#     paragraph = (
#         "A Number has a Factorial.\n"
#         "\tif N is 0:\n"
#         "\t\tthe factorial is 1.\n"
#     )
#     assert lex(paragraph) == [
#         [
#             [
#                 grammar.Determiner('A'),
#                 grammar.Noun('Number'),
#                 grammar.Verb('has'),
#                 grammar.Determiner('a'),
#                 grammar.Noun('Factorial'),
#             ],
#             [
#                 [
#                     grammar.Subordinator('if'),
#                     grammar.Determiner('the'),
#                     grammar.Noun('Number'),
#                     grammar.Verb('is'),
#                     grammar.Number('0'),
#                 ],
#                 [
#                     grammar.Determiner('the'),
#                     grammar.Noun('Factorial'),
#                     grammar.Verb('is'),
#                     grammar.Number('1'),
#                 ]
#             ],
#         ],
#     ]
