
class Relation:
    def __init__(self, name):
        self.name = name

    def dispatch(self, subject, complement, support_sentences):
        """
        :param OrderedSet subject: the subject of the topic sentence
        :param OrderedSet complement: the complement of the topic sentence
        :param str support_sentences: support sentences for the paragraph
        """
        if subject.members or complement.members:
            subject.members = subject.members or subject.kind()
            subject.members = complement.members or complement.kind()
            self.run(subject, complement)
            exec('()\n'.join(support_sentences), subject.scope)
        else:
            self.define(subject, complement, support_sentences)

    def define(self, subject, complement, support_sentences):
        definition = (complement, support_sentences)
        definition_key = self.name + complement.kind.__name__
        setattr(subject.kind, definition_key, definition)

    def definition(self, subject, complement):
        key = self.name + complement.kind.__name__
        try:
            return getattr(subject.kind, key)
        except AttributeError:
            if not hasattr(self.__class__, 'run_python_extension'):
                raise

    def run(self, subject, complement):
        """
        Makes variables in 'scope' available for reading but not writing.
        Makes 'subject' and 'complement' available for reading or writing.
        Executes 'statements'.
        Reverts the global scope to its previous state.
        :param OrderedSet subject: the subject of the sentence being run
        :param OrderedSet complement: the complement of the sentence being run
        """
        saved_complement, statements = getattr(self, subject, complement)
        global_scope = saved_complement.scope
        local_scope = {
            subject.kind.__name__: subject,
            complement.kind.__name__: complement,
        }
        exec('\n'.join(statements), global_scope, local_scope)


class SubjectComplementAgreementError(Exception):
    pass


class MultipleInheritanceError(Exception):
    pass


class Is(Relation):
    def dispatch(self, subject, complement, support_sentences):
        if subject.number != complement.number:
            raise SubjectComplementAgreementError((subject, self, complement))
        super().dispatch(subject, complement, support_sentences)

    def run(self, subject, complement):
        if issubclass(complement.kind, subject.kind):
            for receiver in subject.members:
                receiver.members = complement.members
        else:
            raise TypeError((subject, self, complement))
        super().run(subject, complement)

    def define(self, subject, complement, support_sentences):
        if subject.kind is not Entity:
            raise MultipleInheritanceError((subject, complement))
        name = subject.name
        kind = type(name, (complement.kind,), {})
        subject.scope['nouns'][name].kind = kind
        super().define(subject, complement, support_sentences)


class Has(Relation):
    def run(self, subject, complement):
        for member in subject.members:
            member.relations['has'][complement.kind].add(complement)
        super().run(subject, complement)


class Entity:
    is_ = Is('is_')
    has_ = Has('has_')

    def __init__(self):
        self.relations = {}

    def __eq__(self, other):
        return self.__dict__ == other.__dict__