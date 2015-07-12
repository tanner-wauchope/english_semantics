from plain_english.semantics.complementizer import (
    open_classes,
    Complementizer,
)


def test_complementizer_without_subject():
    that = Complementizer({})
    predicate = that.has
    assert isinstance(predicate, open_classes.Verb)
    assert predicate.verb == 'has'


def test_complementizer_with_subject():
    distributor = type('Distributor, tuple(), {}')()
    that = Complementizer({'every': distributor})
    result = that.every
    assert result is distributor
