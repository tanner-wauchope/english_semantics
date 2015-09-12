from plain_english.semantics.modifiers import That, predicate


def test_complementizer_starting_with_verb():
    that = That({})
    relative_clause = that.has
    assert isinstance(relative_clause, predicate.Predicate)
    assert relative_clause.name == 'has'


def test_complementizer_starting_with_determiner():
    determiner = type('IndefiniteArticle', tuple(), {})()
    that = That({'the': determiner})
    result = that.the
    assert result is determiner