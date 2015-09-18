class NoDefinitionFoundForTypes(TypeError):
    pass


class Relation:
    def __init__(self, name, definitions=None):
        self.name = name
        self.definitions = definitions or []

    def consequences(self, subject, complement):
        result = []
        for definition in self.definitions:
            subject_match = definition.subject.accepts(subject)
            complement_match = definition.complement.accepts(complement)
            if subject_match and complement_match:
                result.append(definition)
        if result:
            return result
        else:
            raise NoDefinitionFoundForTypes

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
        for definition in self.consequences(subject, complement):
            global_scope = definition.subject.scope
            statements = definition.support_text
            local_scope = {
                'nouns': {
                    subject.kind.__name__: subject,
                    complement.kind.__name__: complement,
                }
            }
            lines = statements.split('\n')
            executables = '()\n'.join(lines) + '()'
            exec(executables, global_scope, local_scope)

    def set_relation(self, subject, complement):
        for member in subject.members:
            relation = member.relations[self.name]
            if complement.kind in relation:
                relation[complement.kind].add(complement.members)
            else:
                relation[complement.kind] = complement


class SubjectComplementAgreementError(Exception):
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
        name = subject.name
        kind = type(name, (complement.kind,), {})
        subject.scope['singular'][name].kind = kind
        subject.kind = kind
