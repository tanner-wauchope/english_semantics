from language.syntax.discourse import interpret


def indefinite_article():
    assert interpret("a number") == "a.number"


def definite_article():
    assert interpret("the number") == "the.number"
