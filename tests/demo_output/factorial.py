# A positive integer N has a positive integer factorial.
a(
    positive(integer)
)(Name('N')).has(
    a(
        positive(Integer)
    )(Name('factorial'))
)('.')
# If N is 0,
#     the factorial is 1.
if_(
    N.is_(Cardinal(0))
)(',')(
    the(factorial)._is(Cardinal(1))
)('.')
# Otherwise,
#     the factorial is N times the factorial of the previous integer.
otherwise(',')(
    the(
        factorial
    ).is_(
        N.times(
            the(factorial).of(
                the(
                    previous(Integer)
                )
            )
        )
    )
)