import pytest

from syntax import categories
from syntax.tokenize import (
    InvalidToken,
    classify,
    tokenize,
)


def test_classify_valid():
    assert classify("'") == categories.Clitic
    assert classify('that') == categories.Complementizer
    assert classify('otherwise') == categories.ConjunctiveAdverb
    assert classify('a') == categories.Determiner
    assert classify('it') == categories.Noun
    assert classify('7') == categories.Number
    assert classify('its') == categories.Possessive
    assert classify('"abc"') == categories.Quote
    assert classify('if') == categories.Subordinator
    assert classify('X') == categories.Variable
    assert classify('has') == categories.Verb

def test_classify_invalid():
    with pytest.raises(InvalidToken):
        classify('"abc"abc')
    with pytest.raises(InvalidToken):
        classify("123.123.123")
    with pytest.raises(InvalidToken):
        classify("abc_abc")
    with pytest.raises(InvalidToken):
        classify("'abc'abc")
    with pytest.raises(InvalidToken):
        classify('')


def test_tokenize():
    paragraph = [
        [
            ['A', 'Number', 'N', 'has', 'a', 'Factorial'],
        ]
    ]
    assert tokenize(paragraph) == [
        [
            [
                categories.Determiner('A'),
                categories.Noun('Number'),
                categories.Variable('N'),
                categories.Verb('has'),
                categories.Determiner('a'),
                categories.Noun('Factorial'),

            ]
        ]
    ]
