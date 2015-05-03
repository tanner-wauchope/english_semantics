from plain_english.language.syntax.word import Word


class Complementizer(Word):
    """
    The word class for keywords like "that" and "whose"
    """
    KEYWORDS = {
        'that',
        'whose',
    }

    def complemented_by_word_classes(self):
        """ A complementizer is complemented by a verb. """
        return {'Verb'}

    def complements_word_classes(self):
        """ A complementizer complements a noun. """
        return {'Noun'}
