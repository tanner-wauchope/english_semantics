class Clause(Constituency):
    @property
    def subject(self):
        return self.specifier

    @property
    def verb(self):
        return self.head

    @property
    def object(self):
        return self.complement

    def __repr__(self):
        return '{subject}.{verb}({object})'.format(
            subject=repr(self.subject),
            verb=repr(self.verb),
            object=repr(self.object),
        )
