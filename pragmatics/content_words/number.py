from plain_english.pragmatics.content_words import entity


class Number(entity.Entity):
    """
    I need an init function that takes in an algebraic string
    this class acts like a Decimal object (arbitrary precision)
    """
    pass


class Integer(Number):
    """
    validates that the number is an integer
    compatible with many functions that do not take arbitrary numbers
        indexing, factorial, etc
    provides some integer-specific methods and optimizations
    """
    pass
