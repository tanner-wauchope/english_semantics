from language.syntax.word import Word


keywords = (
    'otherwise',
    'consequently',
)


class ConjunctiveAdverb(Word):
    """
    The word class of keywords like "otherwise".
    """
    def specified_by_word_classes(self):
        """ Subordinators are specified by verbs. """
        return ('Verb')
