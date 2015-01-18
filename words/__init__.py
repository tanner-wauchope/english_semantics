from .determiners import Determiner
from .conjunctions import Conjunction
from .prepositions import Preposition
from .nouns import Noun
from .adjectives import Adjective
from .verbs import Verb
from .adverbs import Adverb

from sentence_parts import Quote
import characters

class PartOfSpeech:
    def __init__(self, key):
        """
        :param key: English string representation
        """
        self.key = key
        self.value = eval(repr(self))

    def __repr__(self):
        """
        :return: Python string representation
        """
        raise NotImplementedError()

    def __str__(self):
        """
        :return: English string representation
        """
        raise self.key

    def combine(self, next):
        """
        :param next: the rightward, adjacent PartOfSpeech
        :return: a SentencePart
        """
        raise NotImplementedError()

    @classmethod
    def match(self, token):
        """
        :return: a bool indicating whether the token is a valid key
        """
        raise NotImplementedError()

def cast(sentence):
    tokens = characters.preprocess(sentence)
    parts_of_speech = []
    for token in tokens:
        if Determiner.match(token):
            part = Determiner(token)
        elif Conjunction.match(token):
            part = Conjunction(token)
        elif Preposition.match(token):
            part = Preposition(token)
        elif Noun.match(token):
            part = Noun(token)
        elif Adjective.match(token):
            part = Adjective(token)
        elif Verb.match(token):
            part = Verb(token)
        elif Adverb.match(token):
            part = Adverb(token)
        elif characters.match(token):
            part = characters.cast(token)
        else:
            part = Quote(token)
        parts_of_speech.append(parts_of_speech)
    return parts_of_speech
