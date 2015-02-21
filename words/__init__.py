from .determiners import Determiner
from .conjunctions import Conjunction
from .prepositions import Preposition
from .nouns import Noun
from .verbs import Verb

class PartOfSpeech:
    def __init__(self, key):
        """
        :param key: English string representation
        """
        self.key = key
        self.value = eval(repr(self))
        self.meanings = [self]

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

