import re

import language
from language.syntax.common import WordClass
from language.syntax.common.numbers import Number
from language.syntax.common.strings import String


STRING = re.compile(r'("(?:[^"\\]|\\.)*")')
NUMBER = re.compile(r'-?\d+(\.\d+)?')
TERM = re.compile(
    r"^(?P<word>[A-Z]?[a-z]+(-[a-z]+)*)"
    r"(?P<punctuation>,|\.|'|'s)?$"
)


class Lexeme:
    def __init__(self, spelling, word_class=None):
        self.spelling = spelling
        self.word_class = word_class

    def __str__(self):
        return self.spelling


class Tokenizer:
    def __init__(self):
        self.local_scope = {}
        self.global_scope = {}
        self.topic = None

    def run(self, block, topics):
        self.local_scope = {}
        lexemes = []
        for string in scan(block):
            if STRING.match(string):
                lexemes.append(Lexeme(string, word_class=String))
            elif NUMBER.match(string):
                lexemes.append(Lexeme(string, word_class=Number))
            else:
                term = TERM.match(string)
                word = term.group(0)
                punctuation = term.group(1)
                lexemes.append(self.lookup(word) or self.define(word))
                lexemes.append(self.lookup(punctuation))
        return lexemes

    def lookup(self, spelling):
        if spelling in self.local_scope:
            return self.local_scope[spelling]
        elif spelling in self.global_scope:
            return self.global_scope[spelling]
        elif hasattr(language, spelling + '_'):
            return getattr(syntax, spelling + '_')

    def define(self, spelling):
        lexeme = Lexeme(spelling, word_class=WordClass)
        if self.topic:
            self.local_scope[spelling] = lexeme
        else:
            self.topic = lexeme
            self.global_scope[spelling] = lexeme
        return lexeme
