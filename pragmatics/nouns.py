import re

from plain_english.pragmatics import verbs


class Noun:
    prototype = {}

    def __init__(self):
        self.predicates = self.prototype.copy()

    def __eq__(self, other):
        self.predicates = other.predicates

    @classmethod
    def new_subclass(cls, name, prototype=None):
        class Subclass(cls):
            prototype = cls.prototype.copy()
        Subclass.prototype.update(prototype or {})
        Subclass.__name__ = name
        return Subclass

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
            self.noun.prototype[item] = verbs.Verb(item[-1:1])
        verb = self.noun.prototype[item]
        return verbs.Clause(self.members, verb)

    def __call__(self, clause):
        if clause.subject:
            return self.query_for_complement(clause)
        else:
            return self.query_for_subject(clause)

    def __eq__(self, other):
        return self.members == other.members

    def __copy__(self):
        result = Group(self.scope, self.noun)
        result.members = list(self.members)
        result.start = self.start
        return result

    def query_for_complement(self, clause):
        """
        :param clause: a clause whose complement is to be queried
        :return: an empty wrapper if the query returns no complements
                 a wrapper of the query's last complement otherwise
        """
        members = clause.subject.query(clause.verb, self.noun)
        return Group(self.scope, members[self.start:])

    def query_for_subject(self, clause):
        """
        :param clause: a clause whose subject is to be queried
        :return: an empty wrapper if the query returns no subjects
                 a wrapper of the query's subjects otherwise
        """
        members = []
        clause.verb = self.noun.prototype[clause.verb]
        for member in self.members:
            if clause.complement == member.query(clause.verb, self.noun):
                members.append(member)
        return Group(self.scope, members[self.start:])
