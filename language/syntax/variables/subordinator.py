from language.syntax.parse import Word


class Subordinator(Word):
    """
    Includes:
        subordinating conjunctions like "if"
        conjunctive adverbs like "otherwise"
    """
    def specifies_word_classes(self):
        """ Subordinators are roots of sentences. """
        return []

    def complements_word_class(self):
        """ Subordinators are roots of sentences. """
        return []