import string


class Text(string.Template):
    """
    interpolates text in []
    any noun phrases can theoretically be interpolated
    See override details at https://docs.python.org/2/library/string.html#template-strings
    """
    def __new__(cls, value, meta):
        pass


class Character(str):
    """
    validates that the constructor string is a single character
    treats everything literally
    use the plural for literal multi-character strings
    provides some character specific methods and optimizations
    """
    def __new__(cls, value, meta):
        pass
