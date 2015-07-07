from plain_english.semantics.function_words import (
    indefinite_article,
    definite_article,
)

def test_getattr():
    scope = {'nouns': {}}
    a = indefinite_article.IndefiniteArticle(scope)
    the = definite_article.DefiniteArticle(scope)
    first_group = a._Factorial_
    scope['nouns']['Factorial'].members.append(first_group.noun())
    second_group = the.Factorial
    assert a.scope['nouns']['Factorial'].members is not second_group.members
    assert len(second_group.members) is 1
    assert isinstance(second_group.members[0], first_group.noun)
