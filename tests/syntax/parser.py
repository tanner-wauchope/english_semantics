from unittest import TestCase

from language.syntax import Clause, NounPhrase
from language.syntax.stages.parse import unify
from language.syntax.stages import parse


class TestParser(TestCase):
    def test_parse(self):
        clause = Clause('exit')
        self.assertEqual(parse('exit'), clause)

    def test_unify(self):
        verb = Clause('say')
        obj = NounPhrase('"hello world"')
        expected_result = Clause('say')
        expected_result.complement = obj
        self.assertEqual(unify([verb, obj]), expected_result)