import decimal


class Number(decimal.Decimal):
    """
    I need an init function that takes in an algebraic string
    this class acts like a Decimal object (arbitrary precision)
    """
    def __new__(cls, value, meta):
        pass


class Integer(int):
    """
    validates that the number is an integer
    compatible with many functions that do not take arbitrary numbers
        indexing, factorial, etc
    provides some integer-specific methods and optimizations
    """
    def __new__(cls, value, meta):
        pass
