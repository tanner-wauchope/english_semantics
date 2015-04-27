from language.syntax.word import Word


keywords = (
    'a',
    'an',
    'any',
    'another',
    'the',
    'each',
)


class Determiner(Word):
    """
    The word class of articles and quantifiers like "each" and "every"
    """
    def specifies_word_classes(self):
        """ Determiners specify word_classes. """
        return ('Noun')
