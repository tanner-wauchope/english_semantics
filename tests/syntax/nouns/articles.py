from unittest import TestCase

from language.syntax import parser
from language.syntax.tokenizer import tokenize


class TestMain(TestCase):
    def test_indefinite_article(self):
        self.assertEqual(
            parser(tokenize("a noun")),
            "a(Noun)"
        )

    def test_definite_article(self):
        self.assertEqual(
            parser(tokenize("the noun")),
            "the(Noun)"
        )
