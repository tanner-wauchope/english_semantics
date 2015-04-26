class Paragraph:
    def __init__(self, sentences, discourse):
        self.sentences = sentences
        self.discourse = discourse
        self.anaphors = {}

    def lines(self):
        for sentence in self.sentences:
            for line in sentence:
                yield line
        raise StopIteration

    def lookup(self, lexeme):
        if lexeme in self.anaphors:
            return (lexeme, self.anaphors[lexeme])
        elif lexeme in self.discourse.topics:
            return (lexeme, self.discourse.topics[lexeme])
        elif hasattr(language, lexeme + '_'):
            return getattr(language, lexeme + '_')
        else:
            raise NameError(lexeme)
