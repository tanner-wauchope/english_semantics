
"""
Since there are many prepositions, I would prefer to not be opinionated about
their meanings. Instead, they can all be defined in terms of related verbs.

Prepositions bind outside of introductory clauses will follow late closure.
Consequently, English sentences will be able to take three arguments.

I'll leave these unfinished for now, but I'll revisit them after verbs are vetted.
"""
prepositions = ('to', 'for_', 'in_', 'on', 'with_', 'of', 'at', 'from')

class Verb:
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


class Clause:
    def __init__(self, subject=None, verb=None, complement=None):
        self.subject = subject
        self.verb = verb
        self.complement = complement

    def __call__(self, complement=None):
        if complement is None or isinstance(complement, str):
            self.verb.dispatch(self, complement)
        else:
            self.complement = complement
            return self
