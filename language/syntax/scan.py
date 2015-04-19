
import language
from language.syntax import try_quote


def quote_split(text):
    """
    :param text: text with an even number of quotation marks
    :return: sequence of texts with the quoted sections separated
    """
    lexemes = ['']
    for character in text:
        is_word = lexemes[-1].startswith('"')
        if character != ' ' or not is_word:
            lexemes[-1] += character
        if character == ' ' and is_word or try_quote(lexemes[-1]):
            lexemes.append('')
    return lexemes


def suffix_split(text, suffix):
    """
    :param text: text to be split into segments
    :param suffix: text that ends each segment
    :return: non-whitespace segments with each suffix preserved
    """
    result = []
    for segment in text.split(suffix):
        if not segment.isspace():
            result.append(segment)
    return result


def scan(text):
    """
    :param text: a block of english text
    :return: a paragraph that holds a tree of lexemes
    """
    sentences = []
    for sentence in suffix_split(text, '.\n'):
        sentences.append([])
        for line in suffix_split(sentence, '\n\t'):
            sentences[-1].append([])
            for lexeme in quote_split(line):
                sentences[-1][-1].append(lexeme)
    return Paragraph(sentences)


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
            return self.anaphors[lexeme]
        elif lexeme in self.discourse.topics:
            return self.discourse.topics[lexeme]
        elif hasattr(language, lexeme + '_'):
            return getattr(language, lexeme + '_')
        else:
            raise NameError(lexeme)