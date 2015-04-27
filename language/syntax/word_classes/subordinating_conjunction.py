from language.syntax.word import Word


keywords = (
    'if',
    'while',
)


class Subordinator(Word):
    """
    The word class of keywords like "if".
    """
    def complemented_by_word_classes(self):
        """ Subordinators are complemented by verbs. """
        return ('Verb')

    def specified_by_word_classes(self):
        """ Subordinators are specified by verbs. """
        return ('Verb')
