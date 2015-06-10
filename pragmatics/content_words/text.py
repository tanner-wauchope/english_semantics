from plain_english.pragmatics.content_words import entity


class Text(entity.Entity):
    """
    interpolates text in []
    """
    pass


class Character(Text):
    """
    validates that the constructor string is a single character
    treats everything literally
    use the plural for literal multi-character strings
    provides some character specific methods and optimizations
    """
    pass
