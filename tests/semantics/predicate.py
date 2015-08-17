import copy

from plain_english.semantics.predicate import (
    entity,
    Predicate,
    OrderedSet,
    That,
)


def test_init_and_eq_for_noun_phrases():
    first = OrderedSet('Factorial')
    assert first.scope == {}
    assert first.kind is entity.Entity
    assert first.members == []
    assert first.number is 1
    second = OrderedSet('Factorial')
    assert first == second
    assert first is not second
    first.members.append(1)
    assert first != second


def test_getattr_for_noun_phrases():
    ordered_set = OrderedSet('Person')
    first = ordered_set._loves_
    assert first.name == '_loves_'
    assert first.subject is ordered_set
    assert isinstance(first, Predicate)
    assert isinstance(ordered_set.kind.loves_, entity.Relation)
    second = ordered_set.loves_
    assert first.subject.kind.loves_ is second.subject.kind.loves_


# def test_relative_clause_with_complement():
#     subject = NounPhrase(members=[1,2,3])
#     complement = NounPhrase(members=[1])
#     verb_phrase = VerbPhrase('is_', complement=complement)
#     subject = subject(verb_phrase)
#     assert subject.members == [1]


# def test_relative_clause_with_subject():
#     subject_members = [entity.Entity()]
#     subject = NounPhrase(members=subject_members)
#     complement = NounPhrase(members=[1])
#     subject.has(complement)
#     verb_phrase = VerbPhrase('has_', subject=subject)
#     assert entity.Entity()(verb_phrase).members == [1]


def test_store_complement_on_noun_phrase():
    noun_phrase = OrderedSet('Factorial')
    verb_phrase = Predicate('does', subject=noun_phrase)
    verb_phrase(noun_phrase)
    assert verb_phrase.complement == noun_phrase


def test_complementizer_starting_with_verb():
    that = That({})
    relative_clause = that.has
    assert isinstance(relative_clause, Predicate)
    assert relative_clause.name == 'has'


def test_complementizer_starting_with_determiner():
    determiner = type('IndefiniteArticle', tuple(), {})()
    that = That({'the': determiner})
    result = that.the
    assert result is determiner
