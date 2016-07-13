import pytest

from plain_english.protolanguage import *


def test_parse():
    # 0 lines
    assert parse([]) == []

    # 1 line
    assert parse(['']) == []
    assert parse(["a b"]) == [['a', 'b']]
    assert parse(["\ta b"]) == [[['a b']]]

    # 2 lines
    assert parse(['', '']) == []
    assert parse(['', 'a']) == [['a']]
    assert parse(['', '\ta']) == [[['', 'a']]]
    assert parse(['a', '']) == [['a']]
    assert parse(["a", "b"]) == [['a'], ['b']]
    assert parse(["a", "\tb"]) == [['a', [['b']]]]
    assert parse(['\ta', '']) == [[['a', '']]]
    assert parse(["\ta", "b"]) == [[['a']], ['b']]
    assert parse(["\ta", "\tb"]) == [[['a', 'b']]]


def test_lookup():
    # degenerate input
    assert lookup(['a'], [None]) == None

    # 0 arguments
    scope = [None]
    definition = ['a', ['b']]
    scope.append((scope, definition))
    assert lookup(['a'], scope) == (scope, definition)

    # 1 argument
    scope = [None]
    definition = ['evaluate', 'A', ['A']]
    scope.append((scope, definition))
    assert lookup(['evaluate', 'B'], scope) == (scope, definition)

    # 2 arguments
    scope = [None]
    definition = ['(', 'A', ')', ['A']]
    scope.append((scope, definition))
    assert lookup(['(', 'B', ')'], scope) == (scope, definition)


def test_evaluate():
    # # undefined input
    # with pytest.raises(SyntaxError):
    #     assert evaluate(['a'], [None]) == None
    #
    # # literal
    # assert evaluate([['a']], [None]) == ['a']
    #
    # # define and then apply a 0-argument function
    # scope = [None]
    # definition = ['a', ['\tb']]
    # evaluate(definition, scope)
    # assert evaluate(['a'], scope) == ['b']

    # define and then apply a 1-argument function
    scope = [None]
    definition = ['evaluate', 'A', ['A']]
    evaluate(definition, scope)
    assert evaluate(['evaluate', ['\tb']], scope) == ['b']
    assert evaluate(['A'], scope) == ['b']

    # # 2 arguments
    # scope = [None]
    # definition = ['(', 'A', ')', [['A']]]
    # scope.append((scope, definition))
    # assert evaluate(['(', 'B', ')'], scope) == (scope, definition)

