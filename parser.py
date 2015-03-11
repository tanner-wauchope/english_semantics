from .words import _you, _all

class Sentence:
    def __init__(self):
        self.words = []
        self.constituencies = []

    def assimilate(self, word):
        self.words.append(word)
        self.constituencies.append(Constituency(word))
        self.unify()

    def unify(self):
        combination = True
        while len(self.constituencies) > 1 and combination:
            second_to_last, last = self.constituencies[-2:]
            combination = second_to_last.combine(last)
            if combination:
                self.constituencies[:-2] = [combination]


class Word:
    COMPLEMENTS = []
    SPECIFIES = []
    REQUIRES_SPECIFIER = False
    REQUIRES_COMPLEMENT = False
    DEFAULT_SPECIFIER = None
    DEFAULT_COMPLEMENT = None

    def __init__(self, spelling, meaning, **kwargs):
        self.spelling = spelling
        self.meaning = meaning
        self._complements = kwargs.get("Complements")
        self._specifies = kwargs.get("Specifies")
        self._complement_default = kwargs.get("Complement Default")
        self._specifier_default = kwargs.get("Specifier Default")

    def __str__(self):
        return self.spelling

    @property
    def complements_types(self):
        if self._complements is not None:
            return self._complements
        return self.__class__.COMPLEMENTS

    @property
    def specifies_types(self):
        if self._specifies is not None:
            return self._specifies
        return self.__class__.SPECIFIES

    @property
    def default_complement(self):
        if self._default_complement:
            return self._default_complement()
        elif self.__class__.DEFAULT_COMPLEMENT:
            return self.DEFAULT_COMPLEMENT()

    @property
    def default_specifier(self):
        if self._default_specifier:
            return self._default_specifier()
        elif self.__class__.DEFAULT_SPECIFIER:
            return self.DEFAULT_SPECIFIER()

    def complements(self, other):
        for Type in self.complements_types():
            if isinstance(other, Type):
                return True

    def specifies(self, other):
        for Type in self.specifies_types():
            if isinstance(other, Type):
                return True

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


class Verb(Word):
    REQUIRES_SPECIFIER = True
    DEFAULT_SPECIFIER = _you
    SPECIFIES = [Subordinator]
    COMPLEMENTS = [Noun, Subordinator] # Relative and subordinate clauses


class TransitiveVerb(Verb):
    REQUIRES_COMPLEMENT = True


class Copula(TransitiveVerb):
    pass


class Pre position(Word):
    """ before, after """
    SPECIFIES = [Noun]
    COMPLEMENTS = [Noun, Copula]


class Operator(Preposition):
    """ plus, minus, times, over """
    COMPLEMENTS = [Noun]


class Complementizer(Word):
    SPECIFIES = [Verb]


class Subordinator(Word):
    REQUIRES_SPECIFIER = True
    REQUIRES_COMPLEMENT = True

###

class Clause(Constituency):
    @property
    def subject(self):
        return self.specifier

    @property
    def verb(self):
        return self.head

    @property
    def object(self):
        return self.complement

    def __repr__(self):
        return '{subject}.{verb}({object})'.format(
            subject=repr(self.subject),
            verb=repr(self.verb),
            object=repr(self.object),
        )


class NounPhrase(Constituency):
    @property
    def determiner(self):
        return self.specifier

    @property
    def noun(self):
        return self.head

    @property
    def operator(self):
        return self.complement

    def __repr__(self):
        return 'WorkSet({determiner} {noun}){operator}'.format(
            subject=repr(self.determiner), # includes a trailing comma
            verb=repr(self.noun),
            object=repr(self.operator),
        )

    def create_clause(self, verb_phrase):
        if self.cardinality() is verb_phrase.cardinality():
            return Clause(self, verb_phrase)
        raise SyntaxError(str(self) + " disagrees with " + str(verb_phrase))


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

