from unittest import TestCase

from language.syntax.stages.tokenize import STRING, NUMBER, WORD, split_by_unquoted_whitespace
from language.syntax.stages import tokenize


class TestLexer(TestCase):
    def test_string_valid(self):
        # Empty quotes
        self.assertIsNotNone(STRING.match('""'))
        # Whitespace
        self.assertIsNotNone(STRING.match('" \t\n "'))
        # Escaped double quotes
        self.assertIsNotNone(STRING.match(r'" \" "'))
        # Single quotes
        self.assertIsNotNone(STRING.match('''" ' "'''))
        # Letters, numbers, and punctuation
        self.assertIsNotNone(STRING.match('" abc, 123. "'))

    def test_string_invalid(self):
        # Empty strings
        self.assertIsNone(STRING.match(''))
        # Unquoted string
        self.assertIsNone(STRING.match('abc'))
        # Strings missing an opening double quote
        self.assertIsNone(STRING.match('abc"'))
        # Strings missing a closing double quote
        self.assertIsNone(STRING.match(r'"abc'))

    def test_number_valid(self):
        # Leading zeros
        self.assertIsNotNone(NUMBER.match('000'))
        # Positive integers
        self.assertIsNotNone(NUMBER.match('123'))
        # Negative integers
        self.assertIsNotNone(NUMBER.match(r'-123'))

        # Trailing zeros
        self.assertIsNotNone(NUMBER.match('.000'))
        # Positive decimals without a leading whole number
        self.assertIsNotNone(NUMBER.match('.123'))
        # Negative decimals without a leading whole number
        self.assertIsNotNone(NUMBER.match('-.123'))

        # Leading and trailing zeros
        self.assertIsNotNone(NUMBER.match('000.000'))
        # Positive decimals with a leading whole number
        self.assertIsNotNone(NUMBER.match('123.123'))
        # Negative decimals with a leading whole number
        self.assertIsNotNone(NUMBER.match('-123.123'))

    def test_number_invalid(self):
        # Empty strings
        self.assertIsNone(NUMBER.match(''))
        # Numbers with a trailing decimal
        self.assertIsNone(NUMBER.match('123.'))
        # Numbers with multiple decimal points
        self.assertIsNone(NUMBER.match('123.123.123'))

    def test_word_valid(self):
        # Lowercase word
        self.assertIsNotNone(WORD.match('abc'))
        # Uppercase word
        self.assertIsNotNone(WORD.match('Abc'))
        # Hyphenated word
        self.assertIsNotNone(WORD.match('abc-abc'))
        # Singular possessive word
        self.assertIsNotNone(WORD.match("abc's"))
        # Plural possessive word
        self.assertIsNotNone(WORD.match("abc'"))
        # Comma-conjoined word
        self.assertIsNotNone(WORD.match('abc,'))
        # Period-conjoined word
        self.assertIsNotNone(WORD.match('abc.'))

    def test_word_invalid(self):
        # Empty strings
        self.assertIsNone(WORD.match(''))
        # Strings with leading hyphens
        self.assertIsNone(WORD.match('-abc'))
        # Strings with trailing hyphens
        self.assertIsNone(WORD.match('abc-'))
        # Acronyms
        self.assertIsNone(WORD.match('ABC'))
        # Numbers
        self.assertIsNone(WORD.match('123'))
        # Un-conjoined apostrophe
        self.assertIsNone(WORD.match("'"))
        # Un-conjoined comma
        self.assertIsNone(WORD.match(','))

    def test_split_by_unquoted_whitespace(self):
        sentence = 'the console says "hello world"'
        actual_result = split_by_unquoted_whitespace(sentence)
        expected_result = [
            'the',
            'console',
            'says',
            '"hello world"',
        ]
        self.assertEqual(actual_result, expected_result)

    def test_tokenize(self):
        actual_result = tokenize('123 "abc" exit')
        expected_result = [123, "abc", _exit]
        self.assertEqual(actual_result, expected_result)