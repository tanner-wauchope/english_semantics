from re import match

from plain_english.python.categories import (
    python,
    Quote,
    Number,
)


# def test_python():
#     raise NotImplementedError
#
#
# class TestClitic:
#     def test_python(self):
#         raise NotImplementedError
#
#
# class TestComplementizer:
#     def test_python(self):
#         raise NotImplementedError
#
#
# class TestAnd:
#     def test_python(self):
#         raise NotImplementedError
#
#
# class TestOr:
#     def test_python(self):
#         raise NotImplementedError
#
#
# class TestDeterminer:
#     def test_python(self):
#         raise NotImplementedError
#
#
# class TestNoun:
#     def test_python(self):
#         raise NotImplementedError
#
#
# class TestNumber:
#     def test_python(self):
#         raise NotImplementedError
#
#
# class TestPreposition:
#     def test_python(self):
#         raise NotImplementedError
#
#
# class TestSubordinator:
#     def test_python(self):
#         raise NotImplementedError
#
#
# class TestVerb:
#     def test_python(self):
#         raise NotImplementedError


class TestQuote:
    def test_valid(self):
        pattern = Quote.PATTERN + '$'
        # Empty quotes
        assert match(pattern, '""')
        # Whitespace
        assert match(pattern, '" \t\n "')
        # Escaped double quotes
        assert match(pattern, r'" \" "')
        # Single quotes
        assert match(pattern, '''" ' "''')
        # Letters, numbers, and punctuation
        assert match(pattern, '" abc, 123. "')

    def test_invalid(self):
        pattern = Quote.PATTERN + '$'
        # Empty strings
        assert not match(pattern, '')
        # Unquoted string
        assert not match(pattern, 'abc')
        # Strings missing an opening double quote
        assert not match(pattern, 'abc"')
        # Strings missing a closing double quote
        assert not match(pattern, r'"abc')


class TestNumber:
    def test_valid(self):
        pattern = Number.PATTERN + '$'
        # Leading and trailing zeros
        assert match(pattern, '000.000')
        # Positive decimals with a leading whole numbers
        assert match(pattern, '123.123')
        # Negative decimals with a leading whole numbers
        assert match(pattern, '-123.123')

    def test_invalid(self):
        pattern = Number.PATTERN + '$'
        # Empty strings
        assert not match(pattern, '')
        # Numbers with multiple decimal points
        assert not match(pattern, '123.123.123')
