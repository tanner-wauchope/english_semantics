from language.syntax.discourse import interpret

def quantifier():
    assert interpret("two numbers") == "two(numbers)"

def constant():
    assert interpret("it is 2") == "it.is(2)"
