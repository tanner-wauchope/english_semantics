import re

characters = '"()<>[],'

def preprocess(sentence):
    for character in characters:
        sentence = sentence.replace(character, ' ' + character + ' ')
    return sentence.split()

def match(token):
    return token in characters

def cast(token):
    pass
