import collections


class NoDefinitionFoundForTypes(TypeError):
    pass


def ancestors(kind):
    # multiple inheritance is not allowed
    if kind.__bases__:
        return ancestors(kind.__bases__[0]) + [kind]
    return [kind]


class Relation:
    def __init__(self, name, definitions):
        self.name = name
        self.definitions = definitions

    def consequents(self, subject, complement):
        result = []
        for subject_ancestor in ancestors(subject.kind):
            for complement_ancestor in ancestors(complement.kind):
                key = (subject_ancestor, complement_ancestor)
                if key in self.definitions:
                    definition = self.definitions[key]
                    saved_subject, saved_complement, statements = definition
                    if saved_subject.accepts(subject) and \
                            saved_complement.accepts(complement):
                        result.append((saved_subject.scope, statements))
        return result
        # try:
        #     key = self.name + complement_kind.__name__
        #     return getattr(subject_kind, key)
        # except AttributeError:
        #     parent_kind = complement_kind.__bases__[0]
        #     return self.definitions(subject_kind, parent_kind)
        # except IndexError:
        #     raise NoDefinitionFoundForTypes

    def run(self, subject, complement):
        if subject.full() and not complement.full():
            complement.instantiate()
        elif not subject.full() and complement.full():
            subject.instantiate()
        if subject.full() and complement.full():
            self.run_eagerly(subject, complement)

    def run_eagerly(self, subject, complement):
        """
        Makes variables in 'scope' available for reading but not writing.
        Makes 'subject' and 'complement' available for reading or writing.
        Executes 'statements'.
        Reverts the global scope to its previous state.
        :param OrderedSet subject: the subject of the sentence being run
        :param OrderedSet complement: the complement of the sentence being run
        """
        self.set_relation(subject, complement)
        for global_scope, statements in self.consequents(subject, complement):
            # TODO: remove the 'nouns' sub-dictionary
            local_scope = {
                'nouns': {
                    subject.kind.__name__: subject,
                    complement.kind.__name__: complement,
                }
            }
            lines = statements.split('\n')
            executables = '()\n'.join(lines) + '()'
            exec(executables, global_scope, local_scope)
            # exec(statements, global_scope, local_scope)

    def set_relation(self, subject, complement):
        for member in subject.members:
            relation = member.relations[self.name]
            if complement.kind in relation:
                relation[complement.kind].add(complement.members)
            else:
                relation[complement.kind] = complement

class SubjectComplementAgreementError(Exception):
    pass


class MultipleInheritanceError(Exception):
    pass


class MutationError(Exception):
    pass


class Is(Relation):
    def run(self, subject, complement):
        if (subject.number is 1) is not (complement.number is 1):
            raise SubjectComplementAgreementError((subject, self, complement))
        elif not complement.definite():
            self.handle_indefinite_complement(subject, complement)
        super().run(subject, complement)

    def run_eagerly(self, subject, complement):
        self.assign(subject, complement)
        super().run_eagerly(subject, complement)

    def assign(self, subject, complement):
        if subject.members:
            raise MutationError('Values are immutable once set.')
        if not issubclass(complement.kind, subject.kind):
            raise TypeError((subject, self, complement))
        subject.members = complement.members

    def handle_indefinite_complement(self, subject, complement):
        if subject.kind is not Entity:
            raise MultipleInheritanceError((subject, complement))
        name = subject.name
        kind = type(name, (complement.kind,), {})
        subject.scope['nouns'][name].kind = kind
        subject.kind = kind


class Entity:
    is_ = Is('is_', {})
    has_ = Relation('has_', {})

    def __init__(self):
        self.relations = collections.defaultdict(dict)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


