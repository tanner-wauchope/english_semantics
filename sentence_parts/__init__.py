
class Constituency:
    def __init__(self, left, right):
        """
        :param left: The left constituent
        :param right: The right constituent
        :return: A constituency rule that is sensitive to cardinality
        """
        if left.cardinality() is right.cardinality():
            self._left = left
            self._right = right
        else:
            message = str(left) + " doesn't agree with " + str(right)
            raise SyntaxError(message)

    def __str__(self):
        return '"{left} {right}"'.format(
            left=self.left,
            right=self.right,
        )

    def cardinality(self, other):
        return 0

class Sentence(Constituency):
    @property
    def clause(self):
        return self._left

    @property
    def end_punctuation(self):
        return self._right

    def __repr__(self):
        return repr(self.clause)

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

    @staticmethod
    def cast(noun_phrase, verb_phrase):
        if isinstance(verb_phrase.argument, Complement):
            return ComplementClause(noun_phrase, verb_phrase)
        return ObjectClause(noun_phrase, verb_phrase)

class ComplementClause(Clause):
    def combine(self, next):
        if isinstance(next, EndPunctuation):
            return Sentence(self, next)

class ObjectClause(Clause):
    def combine(self, next):
        if isinstance(next, EndPunctuation):
            return Sentence(self, next)
        elif isinstance(next, Complement):
            object = self.verb_phrase.argument.combine(next)
            verb_phrase = VerbPhrase(self.verb_phrase.verb, object)
            return ComplementClause(self.noun_phrase, verb_phrase)

class NounPhrase(Constituency):
    def __repr__(self):
        return repr(self.container())

    def cardinality(self):
        return self.container().cardinality()

class CompoundNounPhrase(NounPhrase):
    @property
    def noun_phrase(self):
        return self._left

    @property
    def complement(self):
        return self._right

    def combine(self, next):
        if isinstance(next, VerbPhrase):
            return Clause.cast(self, next)
        elif isinstance(next, Complement):
            return NounPhrase

class SimpleNounPhrase(NounPhrase):
    @property
    def specifier(self):
        return self._left

    @property
    def head(self):
        return self._right

    def combine(self, next):
        if isinstance(next, VerbPhrase):
            return Clause.cast(self, next)

class Complement(Constituency):
    @property
    def operator(self):
        return self._left

    @property
    def noun_phrase(self):
        return self._right

    def combine(self, next):
        if isinstance(next, SimpleNounPhrase):
            return CompoundNounPhrase(self, next)

    def cardinality(self):
        return self.noun_phrase.container().cardinality()

class Specifier(Constituency):
    @property
    def determiner(self):
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
        return '{verb}({object})'.format(
            verb=repr(self.verb),
            object=repr(self.object),
        )

###########

class Noun(PartOfSpeech):
    pass

class CountableNoun(Noun):
    def workset(self, *subtypes, determiner=None):
        result = Workset(self, *subtypes)
        if determiner:
            result.fill(self.determiner.count())
        return result

class UncountableNoun(Noun):
    def combine(self, next):
        if isinstance(next, PluralCountableNoun):
            return PluralNounPhrase(next.workset(self))
        return SingularNounPhrase(self.workset()).combine(next)

class Determiner(PartOfSpeech):
    def combine(self, next):
        if isinstance(next, UncountableNoun):
            return AttributiveSpecifier(self, next)
        elif isinstance(next, CountableNoun):
            return NounPhrase.cast(
                next.workset(self, next)
            )

class Conjunction(PartOfSpeech):
    pass

class Preposition(PartOfSpeech):
    pass

class Verb(PartOfSpeech):
    pass

class Copula(Verb):
    pass

class SingularCopula(Copula):
    pass

class PluralCopula(Copula):
    pass

class LexicalVerb(Verb):
    pass

class SingularLexicalVerb(LexicalVerb):
    pass

class PluralLexicalVerb(LexicalVerb):
    pass
