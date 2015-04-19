from unittest import TestCase

from language.syntax import parser
from language.syntax.tokenizer import tokenize


class TestMain(TestCase):
    def test_intransitive_verb(self):
        self.assertEqual(
            parser(tokenize("noun does")),
            "Noun.does"
        )

    def test_transitive_verb(self):
        self.assertEqual(
            parser(tokenize("noun does noun")),
            "Noun.does(Noun)"
        )

