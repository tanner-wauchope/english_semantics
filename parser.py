from lexer import tokenize

def parse(block):
    result = ''
    for line in block:
        words = []
        constituencies = []
        for token in tokenize(line):
            words.append(token)
            constituencies.append(Constituency(token))
            constituencies = unify(constituencies)
        result += repr(constituencies[0]) + '\n'
    return result

def unify(constituencies):
    combination = True
    while len(constituencies) > 1 and combination:
        second_to_last, last = constituencies[-2:]
        combination = second_to_last.combine(last)
        if combination:
            constituencies[:-2] = [combination]
    return constituencies




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


class NounPhrase(Constituency):
    @property
    def determiner(self):
        return self.specifier

    @property
    def noun(self):
        return self.head

    @property
    def verb(self):
        return self.complement

    def __repr__(self):
        return 'WorkSet({determiner} {noun}){verb}'.format(
            subject=repr(self.determiner), # includes a trailing comma
            verb=repr(self.noun),
            object=repr(self.operator),
        )


