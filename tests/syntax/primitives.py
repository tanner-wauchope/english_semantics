from unittest import TestCase

from language.syntax import *
from ...language.syntax.constituency import Constituency
from ...language.syntax.parser import Parser
from ...language.syntax.tokenizer import Lexer

class TestMain(TestCase):
    def setUp(self):
        self.parser = Parser()
        self.lexer = Lexer()

    def test_string(self):
        lexemes = self.lexer.run('it is "hello world"')
        actual = self.parser.run(lexemes)
        expected = Constituency(
            is_,
            specifier=it_,
            complement=Constituency("hello world"),
        )
        self.assertEqual(actual, expected)

    def test_number(self):
        lexemes = self.lexer.run('say "hello world"')
        actual = self.parser.run(lexemes)
        expected = Constituency(
            is_,
            specifier=it_,
            complement=Constituency("hello world"),
        )
        self.assertEqual(actual, expected)
