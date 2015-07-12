import copy

from plain_english.semantics.word_classes import (
    entity,
    VerbPhrase,
    NounPhrase,
)


def test_init_copy_and_eq_for_noun_phrases():
    first = NounPhrase()
    assert first.scope == {}
    assert first.kind is entity.Entity
    assert first.members == []
    assert first.selector is 0
    first.members.append(1)
    second = copy.copy(first)
    assert first == second
    assert first is not second


def test_getattr_for_noun_phrases():
    noun_phrase = NounPhrase()
    first = noun_phrase._has_
    assert first.name == 'has'
    assert first.subject is noun_phrase
    assert isinstance(first, VerbPhrase)
    assert isinstance(noun_phrase.kind.prototype['has'], entity.Behavior)
    second = noun_phrase.has
    assert first == second


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
    noun_phrase = NounPhrase()
    verb_phrase = VerbPhrase('does', subject=noun_phrase)
    verb_phrase(noun_phrase)
    assert verb_phrase.complement == noun_phrase


# def test_call_verb_phrase():
#     noun_phrase = NounPhrase({})
#     verb_phrase = VerbPhrase('loves', subject=noun_phrase)
#     verb_phrase(noun_phrase)
#     verb_phrase()
#     assert isinstance(noun_phrase.loves, entity.Behavior)
