from language.syntax.discourse import interpret


def explicit_complementizer():
    assert interpret("number that has") == "number(that(has))"