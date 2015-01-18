
class Word:
    """
    Words dispatch to definitions and production rules.
    """
    def __init__(self, meanings):
        self.meanings = meanings

    def combine(self, other):
        for meaning in self.meanings:
            for other_meaning in other.meanings:
                combination = meaning.combine(other_meaning)
                if combination:
                    return combination
