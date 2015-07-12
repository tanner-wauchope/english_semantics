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
            behavior = self.subject.kind.prototype[self.name]
            behavior.dispatch(self, complement)
        else:
            self.complement = complement
            return self


class NounPhrase:
    def __init__(self, scope=None, kind=None, members=None, selector=0):
        self.scope = scope or {}
        self.kind = kind or entity.Entity
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
        result = NounPhrase(self.scope, self.kind)
        result.members = list(self.members)
        result.selector = self.selector
        return result

    def __getattr__(self, item):
        """
        :param item: the name of a verb or a name wrapped in '_'
        :return: a Verb Phrase with this noun phrase as its subject
                 if 'item' was wrapped in '_',
                    instantiate a Behavior for this class
        """
        if re.match(r"_[a-z]+_$", item):
            name = item[1:-1]
            self.kind.prototype[name] = entity.Behavior(name)
            return VerbPhrase(name, subject=self)
        return VerbPhrase(item, subject=self)

    def __call__(self, clause):
        if clause.subject:
            return self.apply_relative_verb_to_subject(clause)
        else:
            return self.apply_relative_verb_to_complement(clause)

    def apply_relative_verb_to_subject(self, clause):
        """
        :param clause: a relative clause with a subject
        :return: an empty wrapper if the query returns no complements
                 a wrapper of the query's last complement otherwise
        """
        members = clause.subject.query(clause.verb, self.kind)
        return NounPhrase(self.scope, members[self.selector:])

    def apply_relative_verb_to_complement(self, clause):
        """
        :param clause: a relative clause with a complement
        :return: an empty wrapper if the query returns no subjects
                 a wrapper of the query's subjects otherwise
        """
        members = []
        clause.verb = self.kind.prototype[clause.verb]
        for member in self.members:
            if clause.complement == member.query(clause.verb, self.kind):
                members.append(member)
        result = NounPhrase(self.scope, self.kind)
        result.members = members[self.selector:]
        return result


# I'll revisit these later
prepositions = ('to', 'for_', 'in_', 'on', 'with_', 'of', 'at', 'from')
