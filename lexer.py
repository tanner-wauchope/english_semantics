import decimal
import re
import enum

from .words import Word

STRING = re.compile(r'("(?:[^"\\]|\\.)*")')
NUMBER = re.compile(r'-?\d+(\.\d+)?')
WORD = re.compile(
    r"^(?P<base>[A-Z]?[a-z]+(-[a-z]+)*)"
    r"(?P<suffix>,|\.|'|'s)?$"
)

class Punctuation(enum.Enum):
    SINGULAR_GENITIVE = "'s"
    PLURAL_GENITIVE = "'"
    COMMA = ','
    PERIOD = '.'

    @classmethod
    def cast(cls, value):
        for punctuation in cls:
            if punctuation.value == value:
                return punctuation

def quote_split(text):
    result = []
    sections = STRING.split(text)
    for section in sections:
        result.extend(section.split())
    return result

def word_parts(token):
    word_parts = []
    word = WORD.match(token)
    base = word.group('base')
    suffix = word.group('suffix')
    word_parts.append(Word.cast(base))
    if suffix:
        word_parts(Punctuation.cast(suffix))
    return word_parts

def tokenize(self, text):
    tokens = []
    for token in quote_split(text):
        if STRING.match(token):
            tokens.append(token)
        elif NUMBER.match(token):
            tokens.append(decimal.Decimal(token))
        elif WORD.match(token):
            tokens.extend(word_parts(token))
        else:
            raise SyntaxError('Invalid token: ' + token)
    return tokens