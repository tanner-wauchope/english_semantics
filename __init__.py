from lexer import tokenize
from parser import Sentence

package_name = 'English Semantics 0.1'


def parse(block):
    result = ''
    for line in block:
        sentence = Sentence()
        for token in tokenize(line):
            sentence.assimilate(token)
        result += repr(sentence) + '\n'
    return result
