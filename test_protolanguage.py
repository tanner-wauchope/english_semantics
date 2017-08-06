import string

from protolanguage import (
    lex,
    Variable,
    tokenize,
    guess_variable,
)


def test_lex_letters_is_token():
    assert lex(string.ascii_letters) == [string.ascii_letters]


def test_lex_digits_is_token():
    assert lex(string.digits) == [string.digits]


def test_lex_punctuation_is_tokens():
    assert lex(string.punctuation) == list(string.punctuation)


def test_lex_whitespace_is_nothing():
    assert lex(string.whitespace) == []


def test_lex_all_types_is_tokens():
    assert lex('\t- Ab 0.1\n') == ['-', 'Ab', '0', '.', '1']


def test_Variable_is_unique():
    assert Variable('X') != Variable('X')


def test_Variable_has_name():
    assert Variable('X').name == 'X'


def test_Variable_displays_as_name():
    assert str(Variable('X')) == 'X'


def test_tokenize_constants_is_constants():
    lexemes, scope = ['constant', '1', '.'], {}
    tokenize(lexemes, scope)
    assert (lexemes, scope) == (['constant', '1', '.'], {})


def test_tokenize_variable_name_binds_name_to_variable():
    lexemes, scope = ['X'], {}
    tokenize(lexemes, scope)
    assert lexemes[0].name == 'X' and scope['X'] == lexemes[0]


def test_tokenize_unique_names_is_unique_variables():
    lexemes, scope = ['X', 'Y'], {}
    tokenize(lexemes, scope)
    assert lexemes[0] != lexemes[1]


def test_tokenize_identical_names_is_same_variable():
    lexemes, scope = ['X', 'X'], {}
    tokenize(lexemes, scope)
    assert lexemes[0] == lexemes[1] == scope['X']


def test_guess_variable_on_constant_is_empty():
    assert list(guess_variable(['constant'], ['constant'])) == []


def test_guess_variable_matches_variable_to_constants():
    consumer, consumed = (Variable('X'),), ('a', 'b')
    assert list(guess_variable(consumer, consumed)) == [{consumer[0]: consumed}]


def test_guess_variable_yields_ambiguous_possibilities():
    x, y = Variable('X'), Variable('Y')
    consumer, consumed = (x, y), ('a', 'b', 'c')
    expected = [{x: ('a',), y: ('b', 'c')}, {x: ('a', 'b'), y: ('c',)}]
    assert list(guess_variable(consumer, consumed)) == expected
