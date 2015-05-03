from plain_english.language.syntax.stages.scan import split, words, lexemes, scan

def test_split():
    assert split(' a b c ', ' ') == ['a', 'b', 'c']

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
