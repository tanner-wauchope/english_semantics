from . import Verb

def possessive(self, subject, complement):
    """
    param complement: a Group or a callable complement-retriever
    When the key used to lookup a value from the prototype
    dictionary is a verb, the result is a set of instances
    or a function
    """
    if not subject.instances and not complement.instances:
        subject.noun.prototype[self][complement.noun] = complement
    elif subject.instances and not complement.instances:
        for member in complement.instances:
            member.predicates[self][complement.noun] = complement

has_ = Verb('has_', possessive)




























def make_getter(name, cases, domain):
    def getter(self):
        if self.satsifies(domain):
            exception = '_' + name
            if hasattr(self, exception):
                return getattr(self, exception)
            for case in cases:
                if self.satsifies(case):
                    return cases[case]
            else:
                raise NotImplementedError('Unhandled case')
        else:
            raise AttributeError(name)

    getter.__name__ = "get_" + name
    return getter

def make_setter(name):
    def setter(self, value):
        setattr(self, '_' + name, value)

    setter.__name__ = "set_" + name
    return setter

def make_property(complement):
    name = str(complement.head)
    kind = complement.head.kind
    cases = {}
    domain = complement.complement
    setattr(kind, name + '_cases', cases)
    setattr(kind, name + '_domain', domain)

    getter = make_getter(name, cases, domain)
    setter = make_setter(name)
    setattr(kind, name, property(getter, setter))


def have(subject, complement):
    attribute_name = str(complement)
    setattr(subject, attribute_name, make_property(complement))