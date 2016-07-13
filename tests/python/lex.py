import pytest

from plain_english.python import grammar
from plain_english.python.lex import (
    split,
    indentation,
    classify,
    tokenize,
    families_at_outer_level,
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


def test_families_at_outer_level():
    # test level 0 with children at multiple levels
    phrases = [
        grammar.Tree('A:', level=0),
        grammar.Tree('B:', level=1),
        grammar.Tree('C', level=2),
        grammar.Tree('A:', level=0),
        grammar.Tree('B:', level=1),
        grammar.Tree('C', level=2),
    ]
    assert families_at_outer_level(phrases) == [phrases[:3], phrases[3:]]

    # verify that a deindent past the current level causes an error
    with pytest.raises(IndentationError):
        families_at_outer_level(phrases[2:4])


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

# Experimental Parser Changes

import pytest

from plain_english.python.grammar import (
    Tree,
    Clitic,
    Complementizer,
    Determiner,
    Noun,
    Number,
    Quote,
    Subordinator,
    Verb,
)
from plain_english.python.lex import (
    ParsingError,
    first,
    last,
    contains,
    merge,
    garden_path,
    parse,
)


def test_first():
    assert first(Tree('a')) == Tree('a')
    assert first(Tree('b', specifier=Tree('a'))) == Tree('a')
    right_branching_tree = Tree('a', complement=Tree('b'))
    assert first(right_branching_tree) == right_branching_tree


def test_last():
    assert last(Tree('a')) == Tree('a')
    assert last(Tree('a', complement=Tree('b'))) == Tree('b')
    left_branching_tree = Tree('b', specifier=Tree('a'))
    assert last(left_branching_tree) == left_branching_tree


def test_contains():
    assert contains([Noun], Noun('it'))
    assert contains([Verb], Verb('is'))
    assert not contains([Noun], Verb('is'))
    assert not contains([Verb], Noun('it'))


def test_merge_complemented_by():
    actual = merge(Complementizer('that'), Verb('is'))
    expected = Complementizer('that', complement=Verb('is'))
    assert actual == expected
    complement = Verb('has', specifier=Noun('it'))
    actual = merge(Subordinator('if'), complement)
    expected = Subordinator('if', complement=complement)
    assert actual == expected


def test_merge_specifies():
    actual = merge(Determiner('the'), Noun('Number'))
    expected = Noun('Number', specifier=Determiner('the'))
    assert actual == expected
    actual = merge(Determiner('the'), Noun('Number'))
    expected = Noun('Number', specifier=Determiner('the'))
    assert actual == expected
    actual = merge(Clitic("'s"), Noun('Number'))
    expected = Noun('Number', specifier=Clitic("'s"))
    assert actual == expected


def test_merge_complements():
    actual = merge(Verb('is'), Noun('it'))
    expected = Verb('is', complement=Noun('it'))
    assert actual == expected
    actual = merge(Verb('is'), Quote('"abc"'))
    expected = Verb('is', complement=Quote('"abc"'))
    assert actual == expected
    actual = merge(Verb('is'), Number('7'))
    expected = Verb('is', complement=Number('7'))
    assert actual == expected
    actual = merge(Noun('Quote'), Quote('"abc"'))
    expected = Noun('Quote', complement=Quote('"abc"'))
    assert actual == expected
    actual = merge(Noun('Number'), Number('7'))
    expected = Noun('Number', complement=Number('7'))
    assert actual == expected


def test_merge_specified_by():
    actual = merge(Noun('it'), Verb('is'))
    expected = Verb('is', specifier=Noun('it'))
    assert actual == expected
    actual = merge(Verb('is'), Subordinator('if'))
    expected = Subordinator('if', specifier=Verb('is'))
    assert actual == expected
    actual = merge(Noun('Number'), Clitic("'s"))
    expected = Clitic("'s", specifier=Noun('Number'))
    assert actual == expected


def test_merge_error():
    with pytest.raises(ParsingError):
        assert merge(Subordinator('if'), Noun('it'))


def test_garden_path_clause():
    words = [Noun('it'), Verb('has'), Determiner('the'), Noun('quote')]
    actual = garden_path(words)[0]
    expected = Verb(
        'has',
        specifier=Noun('it'),
        complement=Noun(
            'quote',
            specifier=Determiner('the')
        )
    )
    assert actual == expected


def test_garden_path_complementizer():
    words = [Noun('numbers'), Determiner('the'), Noun('quote'), Verb('has')]
    actual = garden_path(words)[0]
    expected = Noun(
        'numbers',
        complement=Verb(
            'has',
            specifier=Noun(
                'quote',
                specifier=Determiner('the')
            )
        )
    )
    assert actual == expected


def test_parse_single_clause():
    paragraph = [
        Determiner('a'),
        Noun('Number'),
        Verb('has'),
        Determiner('a'),
        Noun('Factorial'),

    ]
    actual = parse(paragraph)
    expected = Verb(
        'has',
        specifier=Noun(
            'Number',
            specifier=Determiner('a'),
        ),
        complement=Noun(
            'Factorial',
            specifier=Determiner('a')
        )
    )
    assert actual == expected


def test_parse_error():
    paragraph = [
        Subordinator('if'),
        Noun('it'),
    ]
    with pytest.raises(ParsingError):
        parse(paragraph)
