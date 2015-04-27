from language.syntax.discourse import interpret


def trailing_conditional():
    assert interpret("it has if it has") == "(it.has).if_(it.has)"


def leading_conditional():
    assert interpret("if it has, it has") == "if_(it.has)(it.has)"