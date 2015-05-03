from plain_english.language.syntax.word import Word


class Determiner(Word):
    """
    The word class of articles and quantifiers like "each" and "every"
    """
    KEYWORDS = {
        'a',
        'an',
        'any',
        'another',
        'the',
        'each',
    }

    def specifies_word_classes(self):
        """ Determiners specify word_classes. """
        return {'Noun'}
