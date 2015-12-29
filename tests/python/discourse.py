from plain_english.python.discourse import (
    interpret,
    Discourse,
)

factorial_english = """
a Number has a Factorial.
N is the Number.
if N is 0,
\tthe Factorial is 1.
or,
\tthe Factorial is "N * Factorial(N - 1)".
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
    for line in factorial_english.split('\n')[:-1]:
        discourse.interpret(line)
    assert discourse.interpret('\n') == factorial_python
