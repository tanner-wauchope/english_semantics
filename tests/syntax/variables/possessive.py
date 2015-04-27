from language.syntax.discourse import interpret


def singular_possessive():
    assert interpret("the person's number") == "the.person.number"

def singular_possessive():
    assert interpret("the words' meanings") == "the.words.meanings"