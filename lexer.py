import decimal
import re

from . import Word, Pattern

class Lexer:
    def __init__(self, lexicon={}, context={}):
        self.lexicon = lexicon
        self.context = context

    def pattern_matches(self, text):
        matches = {}
        for pattern in Pattern:
            match = re.match(pattern.value, text)
            if match:
                matches[pattern] = match
        return matches

    def lookup(self, token):
        if token in self.context:
            return self.context[token]
        return self.lexicon[token]

    def cast(self, pattern, token):
        if pattern is Pattern.NUMBER:
            return decimal.Decimal(token)
        elif pattern is Pattern.SHORT_QUOTE:
            return token
        elif pattern is Pattern.WORD:
            return self.lookup[token]

    def next_lexeme(self, text):
        next_lexeme = None
        longest_token = ''
        pattern_matches = self.pattern_matches(text)
        for pattern in pattern_matches:
            token = pattern_matches[pattern].group()
            if len(token) > len(longest_token):
                longest_token = token
                next_lexeme = self.cast(pattern, token)
        return next_lexeme

    def tokenize(self, text):
        result = []
        while text:
            token = self.scan(text)
            text = text[len(token):]
            result.append(token)
        return result

