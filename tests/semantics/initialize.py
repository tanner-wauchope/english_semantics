from plain_english.semantics.initialize import initialize

def test_initialize():
    scope = initialize({})
    assert 'a' in scope
    assert 'an' in scope
    assert 'the' in scope
    assert 'singular' in scope
    assert 'Entity' in scope['singular']
    assert 'Text' in scope['singular']
    assert 'Number' in scope['singular']
    assert 'File' in scope['singular']
    assert 'Entities' in scope
    assert 'Texts' in scope
    assert 'Numbers' in scope
    assert 'Files' in scope
