# Fibonacci is a person that has numbers.
Fibonacci.is_(
    a(Person).that(
        has(Numbers)
    )
)('.')
# The first Fibonacci numbers are 0 and 1.
the(
    Ordinal(1)(Fibonacci.numbers)
).are(
    Cardinal(0).and_(Cardinal(1))
)('.')
# Any other Fibonacci number is the sum of
#     the previous Fibonacci number and
#     the Fibonacci number before that.
any_(
    other(Fibonacci.number)
).is_(
    the(sum_).of(
        the(
            previous(Fibonacci.number)
        ).and_(
            the(Fibonacci.number).before(that)
        )
    )
)('.')