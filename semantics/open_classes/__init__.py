import re

from plain_english.semantics.open_classes import entity


class Verb:
    def __init__(self, subject=None, verb=None, complement=None):
        self.subject = subject
        self.verb = verb
        self.complement = complement

    def __call__(self, complement=None):
        if complement is None or isinstance(complement, str):
            self.verb.dispatch(self, complement)
        else:
            self.complement = complement
            return self


class Noun:
    def __init__(self, scope, entity_class=entity.Entity):
        self.scope = scope
        self.kind = entity_class
        self.members = []
        self.start = None

    def __getattr__(self, item):
        if re.match(r"_[a-z]+_$", item):
            verb = entity.Behavior(item[-1:1])
            self.kind.prototype[item] = verb
        verb = self.kind.prototype[item]
        return Verb(self.members, verb)

    def __eq__(self, other):
        return self.members == other.members

    def __copy__(self):
        result = Noun(self.scope, self.kind)
        result.members = list(self.members)
        result.start = self.start
        return result

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
        return Noun(self.scope, members[self.start:])

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
        return Noun(self.scope, members[self.start:])

# I'll revisit these later
prepositions = ('to', 'for_', 'in_', 'on', 'with_', 'of', 'at', 'from')
