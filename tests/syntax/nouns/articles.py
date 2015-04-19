from unittest import TestCase

from language.syntax import parse
from language.syntax.tokenize import tokenize


class TestMain(TestCase):
    def test_indefinite_article(self):
        self.assertEqual(
            parse(tokenize("a noun")),
            "a(Noun)"
        )

    def test_definite_article(self):
        self.assertEqual(
            parse(tokenize("the noun")),
            "the(Noun)"
        )
