class WordClass:
    def specifies(self, first, second):
        return False

    def complements(self, second, first):
        return False

class UnknownWordClass(WordClass):
    def specifies(self, first, second):
        return True

    def complements(self, second, first):
        return True

