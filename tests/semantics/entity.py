from plain_english.semantics.initialize import initialize
from plain_english.semantics.entity import Entity

def test_noun_definition():
    scope = initialize({})
    a = scope['a']
    an = scope['an']
    superclass_set = an.Entity # simple in this case but could have relative clause
    a._Foo_.is_(superclass_set)('a.Foo.has_(a.Foo)')
    Foo = scope['nouns']['Foo'].kind
    assert Foo is not Entity
    assert issubclass(Foo, Entity)
    saved_complement, statements = scope['nouns']['Foo'].kind.is_Entity
    assert saved_complement == superclass_set
    assert statements == 'a.Foo.has_(a.Foo)'
