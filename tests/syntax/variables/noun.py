from language.syntax.discourse import interpret


def subject():
    assert interpret("it has") == "it.has"


def object():
    assert interpret("has it") == "has(it)"


def subject_and_object():
    assert interpret("it has it") == "it.has(it)"
