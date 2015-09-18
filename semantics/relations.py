def full(noun_phrase):
    return not noun_phrase or noun_phrase.full()


def matches(first_noun_phrase, second_noun_phrase):
    if not first_noun_phrase and not second_noun_phrase:
        return True
    elif first_noun_phrase and second_noun_phrase:
        return first_noun_phrase.accepts(second_noun_phrase)


class NoDefinitionFoundForTypes(TypeError):
    pass


class Relation:
    def __init__(self, name, definitions=None):
        self.name = name
        self.definitions = definitions or []

    def consequences(self, subject, complement):
        result = []
        for definition in self.definitions:
            subject_match = matches(definition.subject, subject)
            complement_match = matches(definition.complement, complement)
            if subject_match and complement_match:
                result.append(definition)
        if result:
            return result
        else:
            raise NoDefinitionFoundForTypes

    def run(self, subject, complement):
        if full(subject) and not full(complement):
            complement.instantiate()
        elif not full(subject) and full(complement):
            subject.instantiate()
        if full(subject) and full(complement):
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
        if complement:
            self.set_relation(subject, complement)
        for definition in self.consequences(subject, complement):
            global_scope = definition.subject.scope()
            statements = definition.support_text
            local_scope = {
                'nouns': {
                    subject.kind.__name__: subject,
                }
            }
            if complement:
                local_scope['nouns'][complement.kind.__name__] = complement
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
        if subject.plural() is not complement.plural():
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
        subject.scope()['singular'][name].kind = kind
        subject.kind = kind
