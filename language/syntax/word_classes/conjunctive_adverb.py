from plain_english.language.syntax.word import Word


class ConjunctiveAdverb(Word):
    """
    The word class of keywords like "otherwise".
    """
    KEYWORDS = {
        'otherwise',
        'consequently',
    }

    def specified_by_word_classes(self):
        """ Subordinators are specified by verbs. """
        return {'Verb'}
