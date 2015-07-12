from plain_english.semantics.complementizer import (
    word_classes,
    Complementizer,
)


def test_complementizer_without_subject():
    that = Complementizer({})
    verb_phrase = that.has
    assert isinstance(verb_phrase, word_classes.VerbPhrase)
    assert verb_phrase.name == 'has'


def test_complementizer_with_subject():
    distributor = type('Distributor, tuple(), {}')()
    that = Complementizer({'every': distributor})
    result = that.every
    assert result is distributor
