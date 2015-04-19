block(
    # A whole number N has a factorial.
    a(whole)(Number)('N').has(a("factorial")),
        # If N is 0,
        if_(N.is_(0))(
            # the factorial is 1.
            the(Factorial).is_(1)),
        # Otherwise,
        otherwise(
            # it is N times the factorial of N minus 1.
            it.is_(N.times(the(factorial).of(N.minus(1))))))

block(
    # What is the factorial of 5?
    what.is_(the(factorial).of(5)))