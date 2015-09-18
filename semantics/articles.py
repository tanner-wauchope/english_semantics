from plain_english.semantics import predicate


class UnsupportedNounForDeterminer(Exception):
    """
    Raise if a determiner encounters a noun that has unsupported qualities.
    Unsupported qualities might include new, singular, or plural.
    """
    pass


class Determiner:
    """
    An Determiner is a keyword that creates a Noun Phrase.
    A Noun Phrase's Determiner controls its definiteness.
    """
    DEFINITE = None

    def __init__(self, scope: dict):
        """
        :param scope: the scope of module instantiating the Article
        """
        self.scope = scope

    def __getattr__(self, item: str) -> predicate.OrderedSet:
        """
        :param item: the name of a noun or a name wrapped in '_'
        :return: a NounPhrase that represents the utterance
        """
        if item in self.scope:
            return self.plural_noun_phrase(item)
        elif item in self.scope['singular']:
            return self.singular_noun_phrase(item)
        elif item.startswith('_') and item.endswith('_'):
            return self.defining_noun_phrase(item[1:-1])
        raise NameError

    def plural_noun_phrase(self, plural: str) -> predicate.OrderedSet:
        """
        :param plural: a plural spelling of a noun
        :return: a plural NounPhrase that uses the noun
        """
        raise UnsupportedNounForDeterminer

    def singular_noun_phrase(self, singular: str) -> predicate.OrderedSet:
        """
        :param singular: a singular spelling of a noun
        :return: a singular Noun Phrase that uses the noun
        """
        raise UnsupportedNounForDeterminer

    def defining_noun_phrase(self, new: str) -> predicate.OrderedSet:
        """
        :param new: the singular spelling of a new noun
        :return: a singular Noun Phrase that uses the new noun
        """
        raise UnsupportedNounForDeterminer


class IndefiniteArticle(Determiner):
    """
    An Indefinite Article constructs an indefinite Noun Phrase.
    An indefinite Noun Phrase introduces a new Entity or a new kind.
    """
    DEFINITE = False

    def singular_noun_phrase(self, singular: str) -> predicate.OrderedSet:
        """
        :param singular: a singular spelling of a noun
        :return: a singular Noun Phrase that introduces an Entity
        """
        phrase = self.scope['singular'][singular]
        return predicate.OrderedSet(
            self,
            singular,
            kind=phrase.kind,
        )

    def defining_noun_phrase(self, new: str) -> predicate.OrderedSet:
        """
        :param new: the singular spelling of a new noun
        :return: a singular Noun Phrase that introduces a kind
        """
        phrase = predicate.OrderedSet(self, pluralize(new))
        self.scope[phrase.name] = phrase
        self.scope['singular'][new] = phrase
        return predicate.OrderedSet(self, new)


class The(Determiner):
    """
    A Definite Article constructs an indefinite Noun Phrase.
    A definite Noun Phrase refers to previously introduced Entities.
    """
    DEFINITE = True

    def singular_noun_phrase(self, singular: str) -> predicate.OrderedSet:
        """
        :param singular: a singular spelling of a noun
        :return: a singular Noun Phrase that refers to a previous Entity
        """
        phrase = self.scope['singular'][singular]
        return predicate.OrderedSet(
            self,
            singular,
            kind=phrase.kind,
            members=list(phrase.members),
        )

    def plural_noun_phrase(self, plural: str) -> predicate.OrderedSet:
        """
        :param plural: a plural spelling of a noun
        :return: a plural Noun Phrase that refers to previous Entities
        """
        phrase = self.scope[plural]
        return predicate.OrderedSet(
            self,
            plural,
            kind=phrase.kind,
            members=list(phrase.members),
        )


def pluralize(singular):
    """
    :param singular: the singular spelling
    :return: the default plural spelling
    """
    if singular.endswith('h'):
        return singular + 'es'
    elif singular.endswith('s'):
        return singular + 'es'
    elif singular.endswith('o') and singular[-2] not in 'aeiou':
        return singular + 'es'
    elif singular.endswith('y') and singular[-2] not in 'aeiou':
        return singular[:-1] + 'ies'
    else:
        return singular + 's'
