# Fibonacci is a person that has numbers.
'Fibonacci'.is_(a(Person).that(has(Numbers)))('.')
# The 1st Fibonacci numbers are 0 and 1.
The('1st')(Fibonacci.numbers).are(0).and_(1)('.')
# Any other Fibonacci number is
Any_(other(Fibonacci.number)).is_(
    # the previous Fibonacci number plus
    the(previous(Fibonacci.number)).plus(
    # the Fibonacci number before that.
    the(Fibonacci.number).before(that)))('.')

# What is the 5th Fibonacci number?
What.is_(the('5th')(Fibonacci.number))('?')
