from language.syntax.word import Word


keywords = (
    'that',
    'whose',
)

class Complementizer(Word):
    """
    The word class for keywords like "that" and "whose"
    """
    def complemented_by_word_classes(self):
        """ A complementizer is complemented by a verb. """
        return ('Verb')

    def complements_word_classes(self):
        """ A complementizer complements a noun. """
        return ('Noun')
