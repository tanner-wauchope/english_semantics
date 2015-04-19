block(
    # A mathematician named Fibonacci has numbers.
    a(Mathematician).named("Fibonacci").has(Numbers),
        # The first Fibonacci numbers are 0 and 1.
        the(first)(Fibonacci.numbers).are(0, 1),
        # Any other Fibonacci number is the sum of the previous two.
        any_(other)(Fibonacci.number).is_(the(sum_).of(the(previous)(two))))

block(
    # What is the 5th Fibonacci number?
    what.is_(the('5th')(Fibonacci.number)))
