from unittest import TestCase

from language.syntax import parser
from language.syntax.tokenizer import tokenize


class TestMain(TestCase):
    def test_explicit_complementizer(self):
        self.assertEqual(
            parser(tokenize("noun that does")),
            "Noun.that(does)"
        )

    def test_implicit_complementizer(self):
        self.assertEqual(
            parser(tokenize("noun noun does")),
            "Noun(Noun.does)"
        )
