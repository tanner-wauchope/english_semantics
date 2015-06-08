
class UnexpectedArgumentError(TypeError):
    pass


class Verb:
    def __init__(self, name, definition=None):
        self.name = name
        self.complements = {}
        self.definition = definition

    def initialize(self, topic_sentence):
        """
        Initializes a new verb so that its definition can later be invoked.
        This involves creating a function that executes the definition.
        :param topic_sentence: the sentence that defines the verb
        """

        def new_definition(subject, complement):
            """
            Makes English globals available for reading but not writing.
            Makes English arguments available for reading or writing.
            Executes the definition overloaded to the complement type.
            Reverts the visibility of added global variables before returning.
            :param subject: the subject in the calling sentence
            :param complement: the complement in the calling sentence
            """
            outer_scope = topic_sentence.subject.scope
            context = outer_scope.keys() & globals().keys()
            globals().update({key: outer_scope[key] for key in context})
            locals()[subject.noun.__name__] = subject
            locals()[complement.noun.__name__] = complement
            exec(self.complements[topic_sentence.complement.noun])
            [globals().pop(key) for key in context]

        self.definition = new_definition

    def procedure(self, topic_sentence, support_sentences):
        subject = topic_sentence.subject
        complement = topic_sentence.complement
        if self.definition:
            if subject.filled() or complement.filled():
                self.definition(topic_sentence, support_sentences)
            else:
                self.complements[complement.noun] = support_sentences
        elif not subject.filled() and not complement.filled():
            self.complements[complement.noun] = support_sentences
            self.initialize(topic_sentence)
        raise UnexpectedArgumentError(topic_sentence)


class Clause:
    def __init__(self, subject=None, verb=None, complement=None):
        self.subject = subject
        self.verb = verb
        self.complement = complement

    def __call__(self, complement):
        if complement is None or isinstance(complement, str):
            self.verb.procedure(self, complement)
        else:
            self.complement = complement
            return self
