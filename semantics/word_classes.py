import re

from plain_english.semantics.primitives import entity


class VerbPhrase:
    """
    Verb phrases represents bindings of arguments to a verb.
    These objects manage when a verb's procedure should be called.
    """

    def __init__(self, name, subject=None, complement=None):
        self.name = name
        self.subject = subject
        self.complement = complement

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __call__(self, complement=None):
        """
        :param complement: a noun phrase, supporting sentences, or None
                           The complement is only None for 1-sentence paragraphs.
        :return: If the complement contains supporting sentences,
                 execute the paragraph and return nothing.
                 Otherwise, store the noun phrase and return this verb.
        """
        if complement is None or isinstance(complement, str):
            behavior = getattr(self.subject.kind, self.name)
            behavior.dispatch(self, complement)
        else:
            self.complement = complement
            return self


class NounPhrase:
    def __init__(self, kind=None, scope=None, members=None, selector=0):
        self.kind = kind or entity.Entity
        self.scope = scope or {}
        self.members = members or []
        self.selector = selector

    def __eq__(self, other):
        return self.members == other.members

    def __copy__(self):
        """
        This copy method copies 2 levels deep.
        This is different than the default 1 level, or
        the arbitrary depth of deepcopy.
        """
        return NounPhrase(
            kind=self.kind,
            scope=self.scope,
            members=self.members,
            selector=self.selector
        )

    def __getattr__(self, item):
        """
        :param item: the name of a verb or a name wrapped in '_'
        :return: a Verb Phrase with this noun phrase as its subject
                 if 'item' was wrapped in '_',
                    instantiate a Behavior for this class
        """
        if re.match(r"_[a-z]+_$", item):
            item = item[1:-1]
            self.kind.prototype[item] = entity.Behavior(item)
        return VerbPhrase(item, subject=self)

    def __call__(self, clause):
        if clause.subject:
            subjects = clause.subject.members
            complements = self.members
            goal = True
        else:
            subjects = self.members
            complements = clause.complement.members
            goal = False
        members = query(clause.verb, goal, subjects, complements)
        return NounPhrase(
            kind=self.kind,
            scope=self.scope,
            members=members[self.selector:]
        )


def query(relation, goal, sources=(), targets=()):
    """
    :param relation: a mapping from sources to targets
    :param goal: True if querying for targets
                 False otherwise
    :param sources: sources to be mapped to targets or something empty
    :param targets: targets to which the sources must map or something empty
    :return:
    """
    result = []
    for source in sources:
        for target in source.does_(relation):
            if not targets or target in targets:
                if goal:
                    result.append(target)
                else:
                    result.append(source)
    return result


# I'll revisit these later
prepositions = ('to', 'for_', 'in_', 'on', 'with_', 'of', 'at', 'from')
