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

    def __call__(self, complement=''):
        """
        :param complement: an ordered set or text containing supporting sentences
                           The complement can be an empty string for 1-sentence paragraphs.
        :return: If the complement is support text,
                 either execute the whole paragraph or define a new verb.
                 Otherwise, store the complement and return this predicate.
        """
        if isinstance(complement, str):
            if self.name == 'has_':
                print('first')
            self.resolve_arguments()
            self.resolve_predicate(complement)
        else:
            if self.name == 'has_':
                print(complement.kind)
            self.complement = complement
            return self

    def resolve_predicate(self, support_sentences):
        """
        A name error is thrown if the name is not formatted correctly.
        Run the topic sentence and support sentences if:
            the name references a behavior and the statement is definite.
        Run the topic sentences and add support sentences to a definition if:
            the name references a behavior and the statement is indefinite.
        Do not run anything and add the support sentences to a definition if:
            the verb name is quoted.
        A name error is thrown non-quoted verb name doesn't reference a behavior.
        """
        previously_defined = hasattr(self.subject.kind, self.name)
        definite = self.subject.definite() or self.complement.definite()
        definition = (self.subject, self.complement, support_sentences)
        if self.name == 'has_':
            print(definite)
        if not self.name.endswith('_'):
            raise NameError(self.name)
        elif previously_defined and definite:
            behavior = getattr(self.subject.kind, self.name)
            behavior.run(self.subject, self.complement)
            lines = support_sentences.split('\n')
            executables = '()\n'.join(lines) + '()'
            exec(executables, self.subject.scope)
        elif previously_defined and not definite:
            behavior = getattr(self.subject.kind, self.name)
            behavior.run(self.subject, self.complement)
            behavior.definitions[self.signature()] = definition
        elif self.name.startswith('_'):
            new_name = self.name[1:]
            patterns = {self.signature(): definition}
            behavior = entity.Relation(new_name, patterns)
            setattr(self.subject.kind, new_name, behavior)
        else:
            raise NameError(self.name)

    def signature(self):
        return self.subject.kind, self.complement.kind

    def resolve_arguments(self):
        self.subject.members = self.subject.resolve()
        if not self.complement:
            self.complement = OrderedSet('', number=0, scope=self.subject.scope)
        else:
            self.complement.members = self.complement.resolve()



class ExceededCardinalityError(Exception):
    pass


class OrderedSet:
    def __init__(self, name, kind=None, number=1, members=None, scope=None):
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
        """
        return Predicate(item, subject=self)

    def __call__(self, complement, eager=False):
        """
        :param complement: a relative clause or
                           a string representing a primitive
        :param eager: whether to query if this group is indefinite
        :return: a group containing a new primitive or
                 a group whose members result from a query or
                 a group with an un-queried relative clause
        """
        if not isinstance(complement, Predicate):
            primitive = self.kind(complement, self.scope)
            self.members = [primitive.format(self.scope)]
            return self
        elif eager or self.members:
            return OrderedSet(
                self.name,
                kind=self.kind,
                members=self.resolve(query(self, complement)),
                scope=self.scope,
            )
        else:
            self.relative_clause = complement
            return self

    def add(self, members):
        self.members.extend(members)
        if len(self.members) > self.number:
            raise ExceededCardinalityError((self, self.members))

    def resolve(self, members=None):
        members = members or self.members
        if self.number is None:
            return members
        else:
            return self.members[-self.number:]

    def copy(self):
        return OrderedSet(
            self.name,
            kind=self.kind,
            members=list(self.members),
            scope=self.scope,
            number=self.number,
        )

    def accepts(self, ordered_set):
        # TODO: should check if the parm satisfies any relative clause on self
        return True

    def instantiate(self):
        complement = self.copy()
        instance = self.kind()
        self.members.append(instance)
        self.scope['nouns'][self.name].members.append(instance)
        self.is_(complement)

    def definite(self):
        return (
            self.members or
            self.number is None or
            self.number > 1
        )

    def full(self):
        return self.name == '' or self.definite()


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
                mappings[entity].append(image)
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
        return Predicate(item)


# I'll revisit these later
prepositions = ('to_', 'for_', 'in_', 'of_')
