from language.syntax.primitives import Number, String


class Constituency:
    def __init__(self, head, specifier=None, complement=None):
        self.head = head
        self.specifier = specifier
        self.complement = complement

    def __str__(self):
        return '{specifier} {head} {complement}'.format(
            self.specifier,
            self.head,
            self.complement,
        )

    def __repr__(self):
        comment = '# ' + str(self) + '\n'
        return comment + '{specifier}{head}{complement}'.format(
            self.specifier_repr(),
            self.head_repr(),
            self.complement_repr(),
        )

    def specifier_repr(self):
        if self.specifier:
            return '{}.'.format(self.specifier)
        return ''

    def head_repr(self):
        if self.head.word_class is Number:
            return 'Number({})'.format(self.head)
        elif self.head.word_class is String:
            return 'String({})'.format(self.head)
        return str(self.head)

    def complement_repr(self):
        if self.complement:
            return '({})'.format(self.complement)
        return ''

    def combine(self, other):
        if self.specifies(other):
            other.specifier = self
        elif other.complements(self):
            self.complement = other

    def specifies(self, other):
        return (
            not other.specifier and
            self.head.word_class.specifies(self, other)
        )

    def complements(self, other):
        return (
            not self.specifier and
            other.head.word_class.complements(other, self)
        )