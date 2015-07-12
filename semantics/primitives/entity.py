
class ContradictionError(Exception):
    pass


class Behavior:
    def __init__(self, name, definitions=None):
        self.name = name
        self.definitions = definitions or {} # change this to index on signature

    def lookup(self, signature):
        """
        :param signature: the types of the nouns in the complement
        :return: a definition that matches the signature
        """
        try:
            return self.definitions[signature]
        except KeyError:
            return self.lookup(signature.__bases__[0])
        except IndexError:
            raise ValueError((self, signature))

    def run(self, subject, complement):
        """
        Makes variables in 'scope' available for reading but not writing.
        Makes 'subject' and 'complement' available for reading or writing.
        Executes 'statements'.
        Reverts the global scope to its previous state.
        :param subject: the subject of the sentence being run
        :param complement: the complement of the sentence being run
        """
        definition_globals, statements = self.lookup(complement.noun)
        current_globals = globals()
        copy = dict(current_globals)
        current_globals.update(definition_globals)
        locals()[subject.noun.__name__] = subject
        locals()[complement.noun.__name__] = complement
        exec('\n'.join(statements))
        current_globals = copy

    def define(self, subject, complement, support_sentences):
        definition = (subject.scope, support_sentences)
        self.definitions[complement.noun] = definition

    def dispatch(self, topic_sentence, support_sentences):
        subject = topic_sentence.subject
        complement = topic_sentence.complement
        if subject.members or complement.members:
            subject.members = subject.members or subject.noun()
            subject.members = complement.members or complement.noun()
            self.run(subject, complement)
            exec('\n'.join(support_sentences))
        else:
            self.define(subject, complement, support_sentences)


class Copula(Behavior):
    def run(self, subject, complement):
        if issubclass(complement.noun, subject.noun):
            sets = [sender.values for sender in complement.members]
            package = set.union(*sets)
            for receiver in subject.members:
                if receiver.value and receiver.value != package:
                    raise ContradictionError((receiver.value, package))
                receiver.values = package
        raise TypeError((subject, complement))

    def define(self, subject, complement, support_sentences):
        name = subject.noun.__name__
        noun = type(name, (complement.noun,), {})
        subject.scope['primitives'][name] = noun


class Possessive(Behavior):
    def run(self, subject, complement):
        for member in subject.members:
            current = member.possessions.get(complement.noun)
            if current and current != complement:
                raise ContradictionError
            member.possessions[complement.noun] = complement


class Printer(Behavior):
    pass


class Prompter(Behavior):
    pass


class Entity:
    do = Behavior('do')
    is_ = Copula('is_')
    has_ = Possessive('has_')
    say = Printer('say')
    get = Prompter('get')
    prototype = {}

    def __init__(self):
        self.predicates = self.prototype.copy()

    def __eq__(self, other):
        return self.predicates == other.predicates

    def query(self, verb, noun):
        if verb in self.predicates:
            return self.predicates[verb].complements[noun]