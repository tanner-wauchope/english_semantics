from plain_english.python.discourse import (
    interpret,
    Discourse,
)

factorial_english = """
a Number has a Factorial:
\tN is the Number.
\tif N is 0:
\t\tthe Factorial is 1.
\tor:
\t\tthe Factorial is "N * Factorial(N - 1)".
"""

factorial_python = """
@verb('Number', 'Factorial')
def has(number, factorial):
\tn = noun()
\tn.is_(number)()
\tif_ n.is_(0):
\t\tfactorial.is_(1)()
\telse:
\t\tfactorial.is_("N * Factorial(N - 1)")()
""".strip()


def test_interpret_standalone():
    assert interpret(factorial_english) == factorial_python


def test_interpret_discourse():
    discourse = Discourse()
    for line in factorial_english.split('\n'):
        if line.strip():
            discourse.interpret(line)
    assert discourse.interpret('next paragraph') == factorial_python
