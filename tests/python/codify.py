from plain_english.python import categories
from plain_english.python import codify


def test_clause():
    element = categories.Verb(
        'has',
        specifier=categories.Noun(
            'Number',
            specifier=categories.Determiner('a')
        ),
        complement=categories.Noun(
            'Factorial',
            specifier=categories.Determiner('a')
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
        categories.Subordinator(
            'if',
            complement=categories.Verb(
                'is',
                specifier=categories.Noun('X')
            )
        ),
        categories.Verb(
            'has',
            specifier=categories.Noun('X')
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
            categories.Verb(
                'does',
                specifier=categories.Noun(
                    'Entity',
                    specifier=categories.Determiner('an')
                )
            )
        ],
        [
            categories.Verb(
                'is',
                specifier=categories.Noun(
                    'Entity',
                    specifier=categories.Determiner('the')
                )
            )
        ],
        [
            categories.Subordinator(
                'if',
                complement=categories.Verb(
                    'is',
                    specifier=categories.Noun('X')
                )
            ),
            categories.Verb(
                'has',
                specifier=categories.Noun('X')
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
            categories.Verb(
                'does',
                specifier=categories.Noun(
                    'Entity',
                    specifier=categories.Determiner('an')
                )
            )
        ],
        [
            categories.Verb(
                'is',
                specifier=categories.Noun(
                    'Entity',
                    specifier=categories.Determiner('the')
                )
            )
        ],
        [
            categories.Subordinator(
                'if',
                complement=categories.Verb(
                    'is',
                    specifier=categories.Noun('X')
                )
            ),
            categories.Verb(
                'has',
                specifier=categories.Noun('X')
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