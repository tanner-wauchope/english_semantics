
class Constituency:
    def __init__(self, specifier=None, head=None, complement=None):
        self.specifier = specifier or self.empty_specifier()
        self.head = head or self.empty_specifier()
        self.complement = complement or self.empty_complement()

    def __str__(self):
        return ' '.join(
            str(self.specifier),
            str(self.head),
            str(self.complement),
        )

    def empty_specifier(self):
        return None

    def empty_head(self):
        return None

    def empty_complement(self):
        return None

    def rightmost_unfilled_part(self):
        if self.complement.is_full():
            return None
        elif self.head.is_full():
            return self.complement
        elif self.specifier.is_full():
            return self.head
        else:
            return self.specifier

class Clause(Constituency):
    @property
    def noun_phrase(self):
        return self._left

    @property
    def verb_phrase(self):
        return self._right

    def __repr__(self):
        return '{noun_phrase}.{verb_phrase}'.format(
            subject=repr(self.noun_phrase),
            verb=repr(self.verb_phrase),
        )

    def combine(self, next):
        if isinstance(next, Complement):
            argument = self.verb_phrase.argument.combine(next)
            verb_phrase = self.verb_phrase.verb.combine(argument)
            return self.noun_phrase.combine(verb_phrase)

class NounPhrase(Constituency):
    def create_clause(self, verb_phrase):
        if self.cardinality() is verb_phrase.cardinality():
            return Clause(self, verb_phrase)
        raise SyntaxError(str(self) + " disagrees with " + str(verb_phrase))

class ComplementedNounPhrase(NounPhrase):
    @property
    def noun_phrase(self):
        return self._left

    @property
    def complement(self):
        return self._right

    def cardinality(self):

    def combine(self, next):
        if isinstance(next, VerbPhrase):
            return self.create_clause(next)


class SimpleNounPhrase(Constituency):
    @property
    def specifier(self):
        return self._left

    @property
    def head(self):
        return self._right

    def __repr__(self):
        return '{head}.workset({attribue}, {cardinality})'.format(
            head=str(self.head.meaning.__name__),
            attribute=str(self.specifier.uncountable_noun),
            cardinality=self.cardinality(),
        )

    def cardinality(self):
        if isinstance(self.head, PluralNoun):
            return float('inf')
        elif isinstance(self.head, SingularNoun):
            return 1
        return 0

    def combine(self, next):
        if isinstance(next, Complement):
            return ComplementedNounPhrase(next)
        elif isinstance(next, VerbPhrase):
            return Clause(self, next)


class Complement(Constituency):
    @property
    def preposition(self):
        return self._left

    @property
    def noun_phrase(self):
        return self._right


class Specifier(Constituency):
    @property
    def article(self):
        return self._left

    @property
    def uncountable_noun(self):
        return self._right

    def combine(self, next):
        if isinstance(next, CountableNoun):
            return SimpleNounPhrase(self, next)


class VerbPhrase(Constituency):
    @property
    def verb(self):
        return self._left

    @property
    def argument(self):
        return self._right

    def __repr__(self):
        return '{verb}({argument})'.format(
            verb=repr(self.verb),
            object=repr(self.argument),
        )
