from plain_english.language.pragmatics.verbs import Clause


class Noun:
    prototype = {}

    def __init__(self):
        self.predicates = self.prototype.copy()
        self.group = Group(noun=self)

    def query(self, verb, noun):
        if verb in self.predicates:
            return self.predicates[verb].complements[noun]


class Group:
    def __init__(self, instances=None, start=None, noun=None):
        self.instances = instances or []
        self.start = start
        self.noun = noun or type(instances[0])

    def __getattr__(self, item):
        return Clause(self.instances, self.noun.prototype[item])

    def __call__(self, clause):
        if clause.subject:
            return self.query_for_complement(clause)
        else:
            return self.query_for_subject(clause)

    def query_for_complement(self, clause):
        """
        :param clause: a clause whose complement is to be queried
        :return: an empty wrapper if the query returns no complements
                 a wrapper of the query's last complement otherwise
        """
        instances = clause.subject.query(clause.verb, self.noun)
        return Group(instances[self.start:])

    def query_for_subject(self, clause):
        """
        :param clause: a clause whose subject is to be queried
        :return: an empty wrapper if the query returns no subjects
                 a wrapper of the query's subjects otherwise
        """
        instances = []
        clause.verb = self.noun.prototype[clause.verb]
        for instance in self.noun.group.instances:
            if clause.complement == instance.query(clause.verb, self.noun):
                instances.append(instance)
        return Group(instances[self.start:])
