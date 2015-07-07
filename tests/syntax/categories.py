from re import match

from plain_english.syntax.categories import Quote, Number


def test_quote_valid():
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

def test_quote_invalid():
    pattern = Quote.PATTERN + '$'
    # Empty strings
    assert not match(pattern, '')
    # Unquoted string
    assert not match(pattern, 'abc')
    # Strings missing an opening double quote
    assert not match(pattern, 'abc"')
    # Strings missing a closing double quote
    assert not match(pattern, r'"abc')

def test_number_valid():
    pattern = Number.PATTERN + '$'
    # Leading and trailing zeros
    assert match(pattern, '000.000')
    # Positive decimals with a leading whole numbers
    assert match(pattern, '123.123')
    # Negative decimals with a leading whole numbers
    assert match(pattern, '-123.123')

def test_number_invalid():
    pattern = Number.PATTERN + '$'
    # Empty strings
    assert not match(pattern, '')
    # Numbers with multiple decimal points
    assert not match(pattern, '123.123.123')
