import collections
import re

from plain_english.semantics import entity


class Predicate:
    """
    Verb phrases represents bindings of arguments to a verb.
    These objects manage when a verb's procedure should be called.
    """

    def __init__(self, name, subject=None, complement=None):
        self.name = name
        self.subject = subject
        self.complement = complement

    def __call__(self, complement=None):
        """
        What about intransitive verbs?
        :param complement: an ordered set, supporting sentences, or None
                           The complement is only None for 1-sentence paragraphs.
        :return: If the complement contains supporting sentences,
                 execute the paragraph and return nothing.
                 Otherwise, store the complement and return this predicate.
        """
        if complement is None or isinstance(complement, str):
            behavior = getattr(self.subject.kind, self.name)
            behavior.dispatch(self.subject, self.complement, complement)
        else:
            self.complement = complement
            return self


class ExceededCardinalityError(Exception):
    pass


class OrderedSet:
    def __init__(self, name, kind=None, number=0, members=None, scope=None):
        self.name = name
        self.kind = kind or entity.Entity
        self.members = members or []
        self.scope = scope or {}
        self.number = number

    def __eq__(self, other):
        return self.members == other.members

    def __getattr__(self, item):
        """
        :param item: the name of a verb or a name wrapped in '_'
        :return: a Verb Phrase with this noun phrase as its subject
                 if 'item' was wrapped in '_',
                    instantiate a Behavior for this class
        """
        if re.match(r"_[a-z]+_$", item):
            item = item[1:-1]
            setattr(self.kind, item, entity.Relation(item))
        return Predicate(item, subject=self)

    def __call__(self, clause, eager=False):
        """
        :param clause: a relative clause that complements this group
        :param eager: whether to query if this group is indefinite
        :return: a group whose members result from a query or
                 a group with an un-queried relative clause
        """
        if eager or self.members:
            members = query(self, clause)
            return OrderedSet(
                self.name,
                kind=self.kind,
                members=members[-self.number:],
                scope=self.scope,
            )
        else:
            self.relative_clause = clause
            return self

    def add(self, other):
        self.members[other] = None
        if len(self.members) > self.number:
            raise ExceededCardinalityError((self, self.members))


def query(group, clause):
    """
    :param group: a group being complemented by the clause
    :param clause: a relative clause complementing the group
    :return: the members that the group should have after
             applying the relative clause
    """
    if clause.subject:
        subjects = clause.subject.members
        complements = group.members
        mappings = get_mappings(clause.verb, subjects, complements)
        return [item for group in mappings.values() for item in group]
    else:
        subjects = group.members
        complements = clause.complement.members
        mappings = get_mappings(clause.verb, subjects, complements)
        return mappings.keys()


def get_mappings(function, domain=(), range_=()):
    """
    :param function: a function mapping a source to a target
    :param domain: part of the source or
                   something empty to represent "all"
    :param range_: part of the target or
                   something empty to represent "all"
    :return: the function's mappings from domain to range_ or
             an empty dictionary to represent "all"
    """
    mappings = collections.defaultdict([])
    for entity in domain:
        for image in images(entity, function):
            if not range_ or image in range_:
                mappings[entity].append(image)
    return mappings


def images(entity, function):
    """
    :param entity: an entity that 'does' the function
    :param function: a function that the entity 'does'
    :return: the images that the entity has for the function
    """
    images = []
    for image in entity.target[function]:
        if image.members:
            members = image.members
        elif not image.relative_clause:
            members = image.kind.members
        else:
            members = image(image.relative_clause, eager=True)
        images.extend(members)
    return images


class That:
    def __getattr__(self, item):
        return Predicate(item)


# I'll revisit these later
prepositions = ('to', 'for_', 'in_', 'of')
