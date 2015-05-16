import re

from .noun import Noun


class Ordinal:
    def __init__(self, index):
        self.index = index

    def __getattr__(self, item):
        current = 0
        for reference in DefiniteArticle.discourse:
            if isinstance(reference, Noun.get(item)):
                if current == self.index:
                    return reference
                else:
                    current += 1
        raise IndexError((self.index, item))


class DefiniteArticle:
    first = Ordinal(1)
    second = Ordinal(2)
    third = Ordinal(3)
    fourth = Ordinal(4)
    fifth = Ordinal(5)
    sixth = Ordinal(6)
    seventh = Ordinal(7)
    eighth = Ordinal(8)
    ninth = Ordinal(9)

    def __init__(self):
        self.discourse = []

    def __getattr__(self, item):
        for noun in reversed(self.discourse):
            if noun.name == item:
                self.discourse.append(noun)
                return noun
        if re.match(r"[0-9]+[st|nd|rd|th]", item):
            return Ordinal(int(item[:-2]) - 1)
        raise NameError(item)

the = DefiniteArticle()


class IndefiniteArticle:
    def __init__(self):
        self.namespace = {}

    def __getattr__(self, item):
        if item in self.namespace:
            new = self.namespace[item]()
            the.discourse.append(new)
            return new
        elif re.match(r"_[A-Z][a-z]+_$", item):
            new = Noun(item[1:-1])
            self.namespace[item[1:-1]] = new
            return new
        raise NameError(item)
