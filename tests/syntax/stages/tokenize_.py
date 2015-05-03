import pytest
from plain_english.language.syntax.stages.tokenize import (
    word_classes,
    InvalidToken,
    classify,
    tokenize,
)


def test_classify():
    assert classify('it') == word_classes['Noun']
    with pytest.raises(InvalidToken):
        classify("'abc'abc")


def test_tokenize():
    paragraph = [
        [
            ['A', 'Number', 'N', 'has', 'a', 'Factorial'],
        ]
    ]
    assert tokenize(paragraph) == [
        [
            [
                word_classes['Determiner']('A'),
                word_classes['Noun']('Number'),
                word_classes['Variable']('N'),
                word_classes['Verb']('has'),
                word_classes['Determiner']('a'),
                word_classes['Noun']('Factorial'),

            ]
        ]
    ]
