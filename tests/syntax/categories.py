from re import compile

QUOTE = compile(r'"(?:[^"\\]|\\.)*"')
NUMBER = compile(r"[+-]?\d+(\.\d+)?")
WORD = compile(r"[-a-zA-Z]+")


def quote_valid(self):
    # Empty quotes
    assert QUOTE.match('""')
    # Whitespace
    assert QUOTE.match('" \t\n "')
    # Escaped double quotes
    assert QUOTE.match(r'" \" "')
    # Single quotes
    assert QUOTE.match('''" ' "''')
    # Letters, numbers, and punctuation
    assert QUOTE.match('" abc, 123. "')

def quote_invalid(self):
    # Empty strings
    assert not QUOTE.match('')
    # Unquoted string
    assert not QUOTE.match('abc')
    # Strings missing an opening double quote
    assert not QUOTE.match('abc"')
    # Strings missing a closing double quote
    assert not QUOTE.match(r'"abc')

def number_valid(self):
    # Leading and trailing zeros
    assert NUMBER.match('000.000')
    # Positive decimals with a leading whole number
    assert NUMBER.match('123.123')
    # Negative decimals with a leading whole number
    assert NUMBER.match('-123.123')

def number_invalid(self):
    # Empty strings
    assert not NUMBER.match('')
    # Numbers with a trailing decimal
    assert not NUMBER.match('123.')
    # Numbers with multiple decimal points
    assert not NUMBER.match('123.123.123')
