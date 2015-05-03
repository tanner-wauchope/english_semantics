from language.syntax.discourse import interpret


def literal_import():
    assert interpret("hello world") == "hello word"


def say():
    assert interpret('say "hello world"') == 'say("hello word")'


def name():
    assert interpret('quote "hello world"') == 'quote("hello word")'
