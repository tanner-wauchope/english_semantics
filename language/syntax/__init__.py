from scan import scan
from tokenize import tokenize
from parse import parse

it_ = ''
is_ = ''

class Constituency:
    def __init__(self, word):
        self.complements = None
        self._complement = word.complement_default
        self.head = word
        self.specifies = word.specifier_default
        self._specifier = None

    def __str__(self):
        return ' '.join((
            str(self._specifier),
            str(self.head),
            str(self._complement),
        ))

    def __repr__(self):
        if self.head.__class__.REQUIRES_COMPLEMENT and not self._complement:
            raise SyntaxError(
                'A {head_class} requires a complement.'.format(
                    head_class=self.head.__class__,
                )
            )
        return self.python()

    @property
    def complements(self):
        return self._complements

    @complements.setter
    def complements(self, other):
        if self._complements:
            self._complements._complement = None
        if other:
            other._complement = self
        self._complements = other

    @property
    def specifies(self):
        return self._specifies

    @specifies.setter
    def specifies(self, other):
        if self._specifies:
            self._specifies._specifier = None
        if other:
            other._specifier = self
        self._specifies = other

    @property
    def complement(self):
        return self._complement

    @property
    def specifier(self):
        return self._specifier

    def python(self):
        raise NotImplementedError()

    def can_combine(self):
        if self.__class__.REQUIRES_SPECIFIER and not self._specifier:
            raise SyntaxError(
                'A {head_class} requires a specifier.'.format(
                    head_class=self.head.__class__,
                )
            )
        return not self.complements or self.complements.specifier

    def combine(self, other):
        indirect_combination = self.indirect_combine(other)
        direct_combination = self.direct_combine(other)
        if direct_combination and indirect_combination:
            raise SyntaxError("The sentence is grammatically ambiguous.")
        elif indirect_combination:
            return direct_combination
        elif direct_combination:
            return indirect_combination

    def direct_combine(self, other):
        if self.can_combine():
            if not other.specifier and self.head.specifies(other.head):
                self.specifies = other
                return other
            elif not self.complement and other.head.complements(self.head):
                other.complements = self
                return self

    def indirect_combine(self, other):
        if self.complements:
            return self.direct_combine(other)