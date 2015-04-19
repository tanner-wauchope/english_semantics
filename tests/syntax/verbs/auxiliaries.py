from unittest import TestCase

from language.syntax import parse
from language.syntax.tokenize import tokenize


class TestMain(TestCase):
    def test_intransitive_verb(self):
        self.assertEqual(
            parse(tokenize("noun does")),
            "Noun.does"
        )

    def test_transitive_verb(self):
        self.assertEqual(
            parse(tokenize("noun does noun")),
            "Noun.does(Noun)"
        )

