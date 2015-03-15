from parser import Word



class Verb(Word):
    REQUIRES_SPECIFIER = True
    DEFAULT_SPECIFIER = _you
    SPECIFIES = [Subordinator]
    COMPLEMENTS = [Noun, Subordinator] # Relative and subordinate clauses


class TransitiveVerb(Verb):
    REQUIRES_COMPLEMENT = True


class Copula(TransitiveVerb):
    pass