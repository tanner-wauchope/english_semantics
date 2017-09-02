import collections
import io
import string
import sys

from protolanguage import (
    lex,
    Variable,
    tokenize,
    parse,
    guess_variable,
    run,
    main,
)


def test_lex_letters_is_token():
    assert lex(string.ascii_letters) == [string.ascii_letters]


def test_lex_digits_is_token():
    assert lex(string.digits) == [string.digits]


def test_lex_punctuation_is_tokens():
    assert lex(string.punctuation) == list(string.punctuation)


def test_lex_whitespace_is_token():
    assert lex(string.whitespace) == [string.whitespace]


def test_lex_all_types_is_tokens():
    assert lex('\t-Ab 0.1\n') == ['\t', '-', 'Ab', ' ', '0', '.', '1', '\n']


def test_Variable_is_unique():
    assert Variable('X') != Variable('X')


def test_Variable_has_name():
    assert Variable('X').name == 'X'


def test_Variable_displays_as_name():
    assert str(Variable('X')) == 'X'


def test_tokenize_constants_is_constants():
    lexemes, variables = ['constant', '1', '.'], {}
    lexemes, variables = tokenize(lexemes, variables)
    assert (lexemes, variables) == (('constant', '1', '.'), {})


def test_tokenize_variable_name_binds_name_to_variable():
    lexemes, variables = ['X'], {}
    lexemes, variables = tokenize(lexemes, variables)
    assert lexemes[0].name == 'X' and variables['X'] == lexemes[0]


def test_tokenize_unique_names_is_unique_variables():
    lexemes, variables = ['X', 'Y'], {}
    lexemes, _ = tokenize(lexemes, variables)
    assert lexemes[0] != lexemes[1]


def test_tokenize_identical_names_is_same_variable():
    lexemes, variables = ['X', 'X'], {}
    lexemes, variables = tokenize(lexemes, variables)
    assert lexemes[0] == lexemes[1] == variables['X']


def test_parse_definition_is_head_and_block_and_variables():
    block = [['X', 'lives'], ['X', 'is', 'not', 'dead']]
    head, body, variables = parse(block)
    assert head[0] == body[0][0] == variables['X']


def test_guess_variable_on_constant_is_empty():
    assert list(guess_variable(['constant'], ['constant'], {})) == []


def test_guess_variable_matches_variable_to_constants():
    consumer, consumed = (Variable('X'),), ('a', 'b')
    actual = list(guess_variable(consumer, consumed, {}))
    assert actual == [{consumer[0]: consumed}]


def test_guess_variable_yields_ambiguous_possibilities():
    x, y = Variable('X'), Variable('Y')
    consumer, consumed = (x, y), ('a', 'b', 'c')
    expected = [{x: ('a',), y: ('b', 'c')}, {x: ('a', 'b'), y: ('c',)}]
    assert list(guess_variable(consumer, consumed, {})) == expected


def test_recursion_end_to_end():
    sys.stdin = io.StringIO(
        "tanner is a child of glen\n\n"
        "glen is a child of don\n\n"
        "don is a child of lowis\n\n"
        "X is a grandchild of Y\n"
        "	X is a child of Z\n"
        "	Z is a child of Y\n\n")
    db = collections.OrderedDict()
    try:
        main(db)
    except EOFError:
        sys.stdin = sys.__stdin__
    assert run([lex("Who is a grandchild of Someone")], db) == (
        "tanner is a grandchild of don\n"
        "glen is a grandchild of lowis\n")
