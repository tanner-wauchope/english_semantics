
from plain_english.language.syntax import categories
from plain_english.language.syntax.word import Word
from plain_english.language.syntax.parse import (
    first,
    last,
    contains,
)


def test_first():
    assert first(Word('a')) == Word('a')
    assert first(Word('b', specifier=Word('a'))) == Word('a')
    right_branching_tree = Word('a', complement=Word('b'))
    assert first(right_branching_tree) == right_branching_tree


def test_last():
    assert last(Word('a')) == Word('a')
    assert last(Word('a', complement=Word('b'))) == Word('b')
    left_branching_tree = Word('b', specifier=Word('a'))
    assert last(left_branching_tree) == left_branching_tree


def test_contains():
    assert contains([categories.Noun], categories.Noun('it'))
    assert contains([categories.Verb], categories.Verb('is'))
    assert not contains([categories.Noun], categories.Verb('is'))
    assert not contains([categories.Verb], categories.Noun('it'))


def test_merge():
    pass


def test_move():
    pass


def test_garden_path():
    pass


def test_parse():
    pass
