from plain_english.semantics.articles import (
    An,
    The,
)


def test_write_scope():
    a = An({'nouns': {}})
    singular = a._Factorial_
    assert a.scope['nouns']['Factorial'] is not singular
    assert not singular.members
    plural = a.scope['nouns']['Factorials']
    assert plural.kind is singular.kind
    assert plural is not singular


def test_read_scope():
    a = An({'nouns': {}})
    first_noun = a._Factorial_
    second_noun = a.Factorial
    assert first_noun is not second_noun
    assert second_noun is not a.scope['nouns']['Factorial']
    assert second_noun.kind is first_noun.kind
    assert not second_noun.members


def test_the():
    scope = {'nouns': {}}
    a = An(scope)
    the = The(scope)
    first_noun = a._Factorial_
    members = scope['nouns']['Factorial'].members
    members.append(first_noun.kind())
    second_noun = the.Factorial
    assert members is not second_noun.members
    assert members == second_noun.members
    assert isinstance(second_noun.members[0], first_noun.kind)

