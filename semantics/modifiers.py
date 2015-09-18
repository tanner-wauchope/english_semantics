"""
One meaning of "for" ("for X to Y") is analogous to one meaning of "that" ("that X Y").
One meaning of "that" is analogous to one meaning of "to".
    - with the exception that:
        - "X that Y" treats X like a subject unless Y requires otherwise
        - "X to Y" treats X like a complement unless Y requires otherwise
One meaning of "for" is analogous to one meaning of "to".
    - Both can act as adverbial prepositions that introduce a noun phrase.
"""
import collections
from plain_english.semantics import predicate, relations


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
    for argument in domain:
        for image in images(argument, function):
            if not range_ or image in range_:
                mappings[relations].append(image)
    return mappings


def images(argument, function):
    """
    :param argument: an entity that 'does' the function
    :param function: a function that the entity 'does'
    :return: the images that the entity has for the function
    """
    result = []
    for image in argument.relations[function]:
        if image.members:
            members = image.members
        elif not image.relative_clause:
            members = image.kind.members
        else:
            members = image(image.relative_clause, eager=True) # call image
        result.extend(members)
    return result


class That:
    def __init__(self, scope):
        self.scope = scope

    def __getattr__(self, item):
        """
        :param item: the name of a verb or determiner
        :return: the determiner or a predicate with the name of the verb
        """
        if item in ('a', 'an', 'the'):
            return self.scope[item]
        return predicate.Predicate(item, query=query)


# I'll revisit these later
prepositions = ('to_', 'for_', 'in_', 'of_')