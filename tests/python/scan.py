import pytest

from plain_english.python.scan import (
    InvalidParagraph,
    InvalidSentence,
    validate_paragraph,
    validate_sentence,
    closed,
    lexemes,
)
from plain_english.python.scan import scan


def test_validate_paragraph():
    with pytest.raises(InvalidParagraph):
        validate_paragraph('abc.\n abc\n')


def test_validate_sentence():
    with pytest.raises(InvalidSentence):
        validate_sentence('abc \n abc,\n\t abc')


def test_closed():
    assert closed('"ab') == False
    assert closed('"abc"') == True
    assert closed('(pl. matrices') == False
    assert closed('(pl. matrices)') == True


def test_lexemes():
    assert lexemes("word's plural form") == ['word', "'s", "plural", 'form']
    assert lexemes('it is "words"') == ['it', 'is', '"words"']


def test_scan():
    paragraph = (
        "A whole numbers N has a factorial.\n"
        "If N is 0,\n"
        "\tthe factorial is 1.\n"
        "Otherwise,\n"
        "\tit is N times the factorial of N minus 1.\n"
    )
    assert scan(paragraph) == [
        [
            ['A', 'whole', 'numbers', 'N', 'has', 'a', 'factorial'],
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
