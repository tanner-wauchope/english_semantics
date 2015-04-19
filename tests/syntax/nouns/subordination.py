from unittest import TestCase

from language.syntax import parse
from language.syntax.tokenize import tokenize


class TestMain(TestCase):
    def test_explicit_complementizer(self):
        self.assertEqual(
            parse(tokenize("noun that does")),
            "Noun.that(does)"
        )

    def test_implicit_complementizer(self):
        self.assertEqual(
            parse(tokenize("noun noun does")),
            "Noun(Noun.does)"
        )
