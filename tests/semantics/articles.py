from plain_english.semantics.articles import (
    An,
    The,
)


def test_write_scope():
    a = An({'singular': {}})
    singular = a._Factorial_
    assert not singular.members
    plural = a.scope['Factorials']
    assert plural is not singular
    assert plural.kind is singular.kind


def test_read_scope():
    a = An({'singular': {}})
    first_phrase = a._Factorial_
    second_phrase = a.Factorial
    assert first_phrase is not second_phrase
    assert second_phrase is not a.scope['Factorials']
    assert second_phrase.kind is first_phrase.kind
    assert not second_phrase.members


def test_the():
    scope = {}
    scope['singular'] = {}
    a = An(scope)
    the = The(scope)
    indefinite_phrase = a._Factorial_
    plural = scope['Factorials']
    plural.members.append(plural.kind())
    definite_phrase = the.Factorial
    assert plural.members is not definite_phrase.members
    assert plural.members == definite_phrase.members
    assert isinstance(definite_phrase.members[0], indefinite_phrase.kind)

