
from words import PartOfSpeech

class Sentence(PartOfSpeech):
    def __init__(self, clause, extra=None):
        self.clause = clause
        self.extra = None

    def python(self):
        if self.extra:
            return '{subject}.{predicator}({extra})'.format(
                subject=self.clause.noun_phrase.python(),
                verb=self.clause.verb.python(),
                extra=self.extra.python(),
            )
        return self.clause.python()

    def combine(self):
        return None

class Clause(PartOfSpeech):
    def __init__(self, noun_phrase, verb):
        self.noun_phrase = noun_phrase
        self.verb = verb

    def python(self):
        return '{subject}.{predicator}()'.format(
            subject=self.clause.noun_phrase.python(),
            verb=self.clause.verb.python(),
        )

    def combine(self, next):
        if isinstance(next, PrepositionalPhrase):
            return Sentence(self, next)
        elif isinstance(next, NounPhrase):
            return Sentence(self, next)
        elif next is None:
            return Sentence(self)

class SingularSubjectClause(Clause):
    def combine(self, next):
        if isinstance(next, PrepositionalPhrase):
            return Sentence(self, next)
        elif isinstance(next, SingularNounPhrase):
            return Sentence(self, next)

class PluralSubjectClause(Clause):
    def combine(self, next):
        if isinstance(next, PrepositionalPhrase):
            return Sentence(self, next)
        elif isinstance(next, PluralNounPhrase):
            return Sentence(self, next)

class NounPhrase:
    def __init__(self, workset, property=None):
        self.workset = workset
        self.propery = property

    def python(self):
        if self.property:
            return '{operator}({worksets})'.format(
                operator=self.property.python(),
                worksets=self.workset.python()
            )
        return self.workset.python()

    @classmethod
    def cast(workset, property=None):
        end_workset = property.workset() if property else workset
        if end_workset.limit() is 1:
            return SingularNounPhrase(workset, property=property)
        return PluralNounPhrase(workset, property=property)

class PluralNounPhrase(NounPhrase):
    def combine(self, next):
        if isinstance(next, PluralCopula):
            return PluralSubjectClause(self, next)
        elif isinstance(next, PluralLexicalVerb):
            return Clause(self, next)
        elif isinstance(next, Clitic) and not self.property:
            return PossessiveSpecifier(self.workset)

class SingularNounPhrase(NounPhrase):
    def combine(self, next):
        if isinstance(next, SingularCopula):
            return SingularSubjectClause(self, next)
        elif isinstance(next, SingularLexicalVerb):
            return Clause(self, next)
        elif isinstance(next, Conjunction):
            return ConjunctivePhrase(self, next)
        elif isinstance(next, Clitic) and not self.property:
            return PossessiveSpecifier(self.workset)

class ConjunctivePhrase(PartOfSpeech):
    def __init__(self, workset, conjunction):
        self.workset = workset
        self.conjunction = conjunction

    def combine(self, next):
        if isinstance(next, SingularNounPhrase):
            new_workset = self.conjunction.operate(self.workset, next.workset)
            if new_workset.limit() is 1:
                return SingularNounPhrase(new_workset)
            return PluralNounPhrase(new_workset)

class PossessiveSpecifier(PartOfSpeech):
    def __init__(self, workset):
        self.workset = workset

    def combine(self, next):
        if isinstance(next, CountableNoun):
            return NounPhrase.cast(self.workset, property=next)

class AttributiveSpecifier(PartOfSpeech):
    def __init__(self, determiner, uncountable_noun):
        self.determiner = determiner
        self.uncountable_noun = uncountable_noun

    def combine(self, next):
        if isinstance(next, CountableNoun):
            return NounPhrase.cast(
                next.workset(self.determiner, self.uncountable_noun)
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
