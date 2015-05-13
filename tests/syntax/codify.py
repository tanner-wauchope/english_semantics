from plain_english.language.syntax.categories import (
    Clitic,
    Determiner,
    Noun,
    Quote,
    Subordinator,
    Variable,
    Verb,
)
from plain_english.language.syntax.codify import (
    head,
    subordinate,
    coordinate,
    codify,
)

def test_head():
    assert head(Noun("'Factorial'")) == 'Factorial_'
    assert head(Clitic("'s")) == 's'
    assert head(Verb('is')) == 'is_'
    assert head(Noun('Number')) == 'Number'
    assert head(Quote('"abc \" def"')) == "'abc \" def'"


def test_subordinate():
    sentence = Verb(
        'has',
        specifier=Noun(
            'Number',
            specifier=Determiner('a'),
            complement=Variable('N'),
        ),
        complement=Noun(
            "Factorial",
            specifier=Determiner('a')
        )
    )
    actual = subordinate(sentence)
    expected = 'a.Number(N).has(a.Factorial)'
    assert actual == expected


def test_coordinate_clauses():
    clauses = [
        [Verb('is', specifier=Noun('it'))],
        [Verb('has', specifier=Noun('it'))],
    ]
    actual = coordinate(clauses, '\t\t', '"')
    expected = (
        '(\n'
        '\t\t"it.is_",\n'
        '\t\t"it.has")\n'
    )
    assert actual == expected


def test_coordinate_sentences():
    sentences = [
        [Verb('is', specifier=Noun('it'))],
        [Verb('has', specifier=Noun('it'))],
    ]
    actual = coordinate(sentences, '\t', "'''")
    expected = (
        "(\n"
        "\t'''it.is_''',\n"
        "\t'''it.has''')\n"
    )
    assert actual == expected


def test_codify_clause():
    sentence = Verb('has', specifier=Noun('it'))
    actual = codify(sentence)
    expected = subordinate(sentence)
    assert actual == expected


def test_codify_sentence():
    antecedent = Subordinator('if', complement=Verb('is', specifier=Noun('it')))
    consequent = Verb('has', specifier=Noun('it'))
    actual = codify([antecedent, consequent])
    expected = (
        'if_(it.is_)(\n'
        '\t\t"it.has")\n'
    )
    assert actual == expected


def test_codify_paragraph():
    paragraph = [
        [Verb('is', specifier=Noun('it'))],
        [Verb('has', specifier=Noun('it'))],
    ]
    actual = codify(paragraph)
    expected = (
        "it.is_(\n"
        "\t'''it.has''')\n"
        "\n"
    )
    assert actual == expected
