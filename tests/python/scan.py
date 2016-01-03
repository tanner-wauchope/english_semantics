from plain_english.python.scan import (
    closed,
    lexemes,
    scan,
)


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
        "\tIf N is 0,\n"
        "\t\tthe factorial is 1.\n"
        "\tOtherwise,\n"
        "\t\tit is N times the factorial of N minus 1.\n"
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
