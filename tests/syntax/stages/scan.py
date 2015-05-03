import pytest
from plain_english.language.syntax.stages.scan import (
    InvalidParagraph,
    InvalidSentence,
    InvalidClause,
    validate_paragraph,
    validate_sentence,
    validate_clause,
    split,
    words,
    lexemes,
    scan,
)


def test_validate_paragraph():
    with pytest.raises(InvalidParagraph):
        validate_paragraph('abc.\n abc\n')


def test_validate_sentence():
    with pytest.raises(InvalidSentence):
        validate_sentence('abc \n abc,\n\t abc')


def test_validate_clause():
    with pytest.raises(InvalidClause):
        validate_clause('"abc" abc')
    with pytest.raises(InvalidClause):
        validate_clause('abc " abc')


def test_split():
    assert split('a b c ', ' ') == ['a', 'b', 'c']


def test_words():
    assert words("word's plural") == ['word', "'s", 'plural']


def test_lexemes():
    assert lexemes('it is "words"') == ['it', 'is', '"words"']


def test_scan():
    paragraph = (
        "A whole number N has a factorial.\n"
        "If N is 0,\n"
        "\tthe factorial is 1.\n"
        "Otherwise,\n"
        "\tit is N times the factorial of N minus 1.\n"
    )
    assert scan(paragraph) == [
        [
            ['A', 'whole', 'number', 'N', 'has', 'a', 'factorial'],
        ],
        [
            ['If', 'N', 'is', '0'],
            ['the', 'factorial', 'is', '1']
        ],
        [
            ['Otherwise'],
            ['it', 'is', 'N', 'times', 'the', 'factorial', 'of', 'N', 'minus', '1']
        ],
    ]
