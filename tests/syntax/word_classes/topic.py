from language.syntax.discourse import interpret


# maybe i need to disallow defining words based on their position in a sentence.
def topic():
    assert interpret("the 'person'") == "a(person)"
