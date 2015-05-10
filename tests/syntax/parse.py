from plain_english.language.syntax.categories import (
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
from plain_english.language.syntax.word import Word
from plain_english.language.syntax.parse import (
    first,
    last,
    contains,
    merge,
    move,
    garden_path,
    parse,
)


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


def test_move():
    antecedent = Verb('is', specifier=Noun('it'))
    consequent = Verb('has', specifier=Noun('it'))
    subordinate_clause = Subordinator('if', complement=antecedent)
    actual = move(subordinate_clause, consequent)
    expected = Subordinator('if', specifier=consequent, complement=antecedent)
    assert actual == expected


def test_garden_path_clause():
    words = [Noun('it'), Verb('has'), Determiner('the'), Noun('quote')]
    actual, leftover = garden_path(words)
    assert leftover == []
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
    words = [Noun('number'), Determiner('the'), Noun('quote'), Verb('has')]
    actual, leftover = garden_path(words)
    assert leftover == []
    expected = Noun(
        'number',
        complement=Verb(
            'has',
            specifier=Noun(
                'quote',
                specifier=Determiner('the')
            )
        )
    )
    assert actual == expected


def test_parse():
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
    tree = parse(paragraph)[0]
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
    assert tree == expected
