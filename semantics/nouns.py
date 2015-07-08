import re

from plain_english.semantics import verbs


class Noun:
    prototype = {}

    def __init__(self):
        self.predicates = self.prototype.copy()

    def __eq__(self, other):
        self.predicates = other.predicates

    def query(self, verb, noun):
        if verb in self.predicates:
            return self.predicates[verb].complements[noun]


class Group:
    def __init__(self, scope, noun):
        self.scope = scope
        self.noun = noun
        self.members = []
        self.start = None

    def __getattr__(self, item):
        if re.match(r"_[a-z]+_$", item):
            verb = verbs.Verb(item[-1:1])
            self.noun.prototype[item] = verb
        verb = self.noun.prototype[item]
        return verbs.Clause(self.members, verb)

    def __eq__(self, other):
        return self.members == other.members

    def __copy__(self):
        result = Group(self.scope, self.noun)
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
        members = clause.subject.query(clause.verb, self.noun)
        return Group(self.scope, members[self.start:])

    def apply_relative_verb_to_complement(self, clause):
        """
        :param clause: a relative clause with a complement
        :return: an empty wrapper if the query returns no subjects
                 a wrapper of the query's subjects otherwise
        """
        members = []
        clause.verb = self.noun.prototype[clause.verb]
        for member in self.members:
            if clause.complement == member.query(clause.verb, self.noun):
                members.append(member)
        return Group(self.scope, members[self.start:])
