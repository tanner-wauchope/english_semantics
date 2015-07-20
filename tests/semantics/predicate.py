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
    assert first.number is 0
    second = OrderedSet('Factorial')
    assert first == second
    assert first is not second
    first.members.append(1)
    assert first != second


def test_getattr_for_noun_phrases():
    noun_phrase = OrderedSet('Factorial')
    first = noun_phrase._has_
    assert first.name == 'has'
    assert first.subject is noun_phrase
    assert isinstance(first, Predicate)
    assert isinstance(noun_phrase.kind.has, entity.Relation)
    second = noun_phrase.has
    assert first.name == second.name


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


# def test_call_verb_phrase():
#     noun_phrase = NounPhrase({})
#     verb_phrase = VerbPhrase('loves', subject=noun_phrase)
#     verb_phrase(noun_phrase)
#     verb_phrase()
#     assert isinstance(noun_phrase.loves, entity.Behavior)


def test_complementizer():
    that = That()
    relative_clause = that.has
    assert isinstance(relative_clause, Predicate)
    assert relative_clause.name == 'has'

