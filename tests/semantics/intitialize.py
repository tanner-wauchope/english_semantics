from plain_english.semantics.initialize import initialize

def test_initialize():
    scope = initialize({})
    assert 'a' in scope
    assert 'an' in scope
    assert 'the' in scope
    assert 'all' in scope
    assert 'nouns' in scope
    assert 'Entity' in scope['nouns']
    assert 'Text' in scope['nouns']
    assert 'Number' in scope['nouns']