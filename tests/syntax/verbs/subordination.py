from unittest import TestCase

from language.syntax import parse
from language.syntax.tokenize import tokenize


class TestMain(TestCase):
    def test_positive_trailing_conditional(self):
        self.assertEqual(
            parse(tokenize("It does if so.")),
            "it.does.if_(so)"
        )

    def test_positive_leading_conditional(self):
        self.assertEqual(
            parse(tokenize("If so, it does.")),
            "if_(so)(it.does)"
        )

    def test_negative_trailing_conditional(self):
        self.assertEqual(
            parse(tokenize("It does not if not.")),
            "it.does(not).if_(not)"
        )

    def test_negative_leading_conditional(self):
        self.assertEqual(
            parse(tokenize("If not, it does not.")),
            "if_(not).it.does(not)"
        )
