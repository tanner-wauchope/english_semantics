from plain_english.semantics.function_words.indefinite_article import (
    nouns,
    entity,
    IndefiniteArticle,
)

def new_class():
    a = IndefiniteArticle({'nouns': {}})
    group = a._Factorial_
    assert issubclass(nouns.noun, entity.Entity)
    assert group.noun.__name__ == 'Factorial'
    assert a.scope['nouns']['Factorial'] is not group
    assert not group.members


def new_empty_group():
    a = IndefiniteArticle({'nouns': {}})
    first_group = a._Factorial_
    second_group = a.Factorial
    assert first_group is not second_group
    assert isinstance(second_group.members[0], first_group.noun)
    assert len(second_group.members is 0)
