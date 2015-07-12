from plain_english.semantics.indefinite_article import (
    entity,
    IndefiniteArticle,
)


def test_write_scope():
    a = IndefiniteArticle({'nouns': {}})
    noun = a._Factorial_
    assert noun.kind is entity.Entity
    assert a.scope['nouns']['Factorial'] is not noun
    assert not noun.members


def test_read_scope():
    a = IndefiniteArticle({'nouns': {}})
    first_noun = a._Factorial_
    second_noun = a.Factorial
    assert first_noun is not second_noun
    assert second_noun is not a.scope['nouns']['Factorial']
    assert second_noun.kind is first_noun.kind
    assert not second_noun.members
