import pytest

from plain_english.python import categories
from plain_english.python.tokenize import (
    InvalidToken,
    classify,
    tokenize,
)


def test_classify_valid():
    assert classify("'") == categories.Clitic
    assert classify('that') == categories.Complementizer
    assert classify('or') == categories.Or
    assert classify('a') == categories.Determiner
    assert classify('it') == categories.Noun
    assert classify('7') == categories.Number
    assert classify('"abc"') == categories.Quote
    assert classify('if') == categories.Subordinator
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
            ['A', 'Number', 'has', 'a', 'Factorial'],
        ]
    ]
    assert tokenize(paragraph) == [
        [
            [
                categories.Determiner('A'),
                categories.Noun('Number'),
                categories.Verb('has'),
                categories.Determiner('a'),
                categories.Noun('Factorial'),

            ]
        ]
    ]
