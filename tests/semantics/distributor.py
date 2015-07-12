from plain_english.semantics.distributor import (
    open_classes,
    Distributor,
)


def test_distributor():
    scope = {'nouns': {}}
    scope_noun = open_classes.Noun(scope)
    scope_noun.members.append(scope_noun.kind())
    scope['nouns']['Factorial'] = scope_noun
    every = Distributor(scope)
    utterance_noun = every.Factorial
    assert utterance_noun.kind is scope_noun.kind
    assert utterance_noun is not scope_noun
    assert utterance_noun.members == [scope_noun.kind()]

