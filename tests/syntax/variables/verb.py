from language.syntax.discourse import interpret


def implicit_complementizer():
    assert interpret("number it has") == "number(it.has)"
