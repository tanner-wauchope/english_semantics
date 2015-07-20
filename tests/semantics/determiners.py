from plain_english.semantics.determiners import (
    An,
    The,
    All,
)
from plain_english.semantics import predicate


def test_write_scope():
    a = An({'nouns': {}})
    noun = a._Factorial_
    assert a.scope['nouns']['Factorial'] is not noun
    assert not noun.members


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


def test_all():
    scope = {'nouns': {}}
    scope_noun = predicate.OrderedSet('Factorial', scope=scope)
    scope_noun.members.append(scope_noun.kind())
    scope['nouns']['Factorial'] = scope_noun
    all = All(scope)
    utterance_noun = all.Factorial
    assert utterance_noun.kind is scope_noun.kind
    assert utterance_noun is not scope_noun
    assert utterance_noun.members == [scope_noun.kind()]
