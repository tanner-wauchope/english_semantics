from plain_english.semantics import definite_article, indefinite_article


def test_definite_article():
    scope = {'nouns': {}}
    a = indefinite_article.IndefiniteArticle(scope)
    the = definite_article.DefiniteArticle(scope)
    first_noun = a._Factorial_
    members = scope['nouns']['Factorial'].members
    members.append(first_noun.kind())
    second_noun = the.Factorial
    assert members is not second_noun.members
    assert members == second_noun.members
    assert isinstance(second_noun.members[0], first_noun.kind)
