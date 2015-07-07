import pytest

from plain_english.syntax.categories import (
    Clitic,
    Complementizer,
    Determiner,
    Noun,
    Number,
    Quote,
    Subordinator,
    Variable,
    Verb,
)
from plain_english.syntax.word import Word
from plain_english.syntax.parse import (
    PhrasesCannotMerge,
    first,
    last,
    contains,
    merge,
    garden_path,
)
from plain_english.syntax.parse import parse


def test_first():
    assert first(Word('a')) == Word('a')
    assert first(Word('b', specifier=Word('a'))) == Word('a')
    right_branching_tree = Word('a', complement=Word('b'))
    assert first(right_branching_tree) == right_branching_tree


def test_last():
    assert last(Word('a')) == Word('a')
    assert last(Word('a', complement=Word('b'))) == Word('b')
    left_branching_tree = Word('b', specifier=Word('a'))
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
    with pytest.raises(PhrasesCannotMerge):
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
        [
            [
                Determiner('a'),
                Noun('Number'),
                Variable('N'),
                Verb('has'),
                Determiner('a'),
                Noun('Factorial'),

            ]
        ]
    ]
    actual = parse(paragraph)[0][0]
    expected = Verb(
        'has',
        specifier=Noun(
            'Number',
            specifier=Determiner('a'),
            complement=Variable('N'),
        ),
        complement=Noun(
            'Factorial',
            specifier=Determiner('a')
        )
    )
    assert actual == expected


def test_parse_multiple_clause():
    paragraph = [
        [
            [
                Subordinator('if'),
                Noun('it'),
                Verb('is'),
            ],
            [
                Noun('it'),
                Verb('has'),
            ]
        ]
    ]
    actual = parse(paragraph)[0]
    antecedent = Subordinator('if', complement=Verb('is', specifier=Noun('it')))
    consequent = Verb('has', specifier=Noun('it'))
    assert actual == [antecedent, consequent]


def test_parse_error():
    paragraph = [
        [
            [
                Subordinator('if'),
                Noun('it'),
            ],
        ]
    ]
    with pytest.raises(PhrasesCannotMerge):
        parse(paragraph)
