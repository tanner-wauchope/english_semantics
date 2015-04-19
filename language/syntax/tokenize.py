from language.syntax import try_quote, try_float, try_possessive
from language.syntax.common.primitives import Number, String
from language.syntax.nouns.possession import Clitic


class WordClass:
    def specifies(self):
        pass

    def complements(self):
        pass


class Token:
    def __init__(self, spelling, word_class):
        self.spelling = spelling
        self.word_class = word_class


def tokenize(self, paragraph):
    self.local_scope = {}
    for line in paragraph.lines():
        for i, lexeme in enumerate(paragraph.lines()):
            if lexeme.isalpha():
                line[i] = paragraph.lookup(lexeme)
            if try_quote(lexeme):
                line[i] = (lexeme, String)
            elif try_float(lexeme):
                line[i] = (lexeme, Number)
            elif try_possessive(lexeme):
                word, clitic = lexeme.split('"')
                line[i] = paragraph.lookup(word)
                line.insert(i + 1, ("'" + clitic, Clitic))
            else:
                raise NameError(lexeme)
    return paragraph
