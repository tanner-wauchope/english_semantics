from plain_english.python import grammar
from plain_english.python import codify


def test_clause():
    element = grammar.Verb(
        'has',
        specifier=grammar.Noun(
            'Number',
            specifier=grammar.Determiner('a')
        ),
        complement=grammar.Noun(
            'Factorial',
            specifier=grammar.Determiner('a')
        )
    )
    actual = codify.clause(element, codify.Scope())
    expected = [
        "number = noun('Number')",
        "factorial = noun('Factorial')",
        "number.has(factorial)()",
    ]
    assert actual == expected


def test_sentence():
    element = [
        grammar.Subordinator(
            'if',
            complement=grammar.Verb(
                'is',
                specifier=grammar.Noun('X')
            )
        ),
        grammar.Verb(
            'has',
            specifier=grammar.Noun('X')
        )
    ]
    actual = codify.sentence(element, codify.Scope())
    expected = [
        "x = noun()",
        "if_ x.is_:",
        [
            "x.has()"
        ]
    ]
    assert actual == expected


def test_paragraph():
    element = [
        [
            grammar.Verb(
                'does',
                specifier=grammar.Noun(
                    'Entity',
                    specifier=grammar.Determiner('an')
                )
            )
        ],
        [
            grammar.Verb(
                'is',
                specifier=grammar.Noun(
                    'Entity',
                    specifier=grammar.Determiner('the')
                )
            )
        ],
        [
            grammar.Subordinator(
                'if',
                complement=grammar.Verb(
                    'is',
                    specifier=grammar.Noun('X')
                )
            ),
            grammar.Verb(
                'has',
                specifier=grammar.Noun('X')
            )
        ]
    ]
    actual = codify.paragraph(element, codify.Scope())
    expected = [
        "@verb('Entity')",
        "def does(entity):",
        [
            "entity.is_()",
            "x = noun()",
            "if_ x.is_:",
            [
                "x.has()"
            ]
        ]
    ]
    assert actual == expected


def test_flatten():
    element = [
        "@verb('Entity')",
        "def does(entity):",
        [
            "entity.is_()",
            "entity.has()",
            "x = noun()",
            "if_ x.is_:",
                [
                    "x.has()"
                ]
        ],
    ]
    actual = codify.flatten(element)
    expected = [
        "@verb('Entity')",
        "def does(entity):",
        "\tentity.is_()",
        "\tentity.has()",
        "\tx = noun()",
        "\tif_ x.is_:",
        "\t\tx.has()",
    ]
    assert actual == expected


def test_codify():
    element = [
        [
            grammar.Verb(
                'does',
                specifier=grammar.Noun(
                    'Entity',
                    specifier=grammar.Determiner('an')
                )
            )
        ],
        [
            grammar.Verb(
                'is',
                specifier=grammar.Noun(
                    'Entity',
                    specifier=grammar.Determiner('the')
                )
            )
        ],
        [
            grammar.Subordinator(
                'if',
                complement=grammar.Verb(
                    'is',
                    specifier=grammar.Noun('X')
                )
            ),
            grammar.Verb(
                'has',
                specifier=grammar.Noun('X')
            )
        ]
    ]
    actual = codify.codify(element)
    expected = (
        "@verb('Entity')\n"
        "def does(entity):\n"
        "\tentity.is_()\n"
        "\tx = noun()\n"
        "\tif_ x.is_:\n"
        "\t\tx.has()"
    )
    assert actual == expected