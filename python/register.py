
def register() -> tuple:
    """
    :return: a decorator for creating or accessing verbs
             a function for creating or accessing nouns
    """
    nouns = {}

    def noun(name=None) -> Noun:
        """
        :param str name: the name of the noun to get or create
        :return: the noun that has the name or a new noun
        """
        if name is None:
            return Noun()
        entry = nouns.get(name) or type(name, (Noun,), {})
        nouns[name] = entry
        return entry()

    verbs = {}

    def verb(*kinds):
        """
        :param kinds: the signature for definitions the returned function adds
        :return: a function that adds new definitions to verbs
        """
        def define(function) -> Verb:
            """
            :param callable function: a new definition for a verb
            :return: the verb whose name is the function's name or a new verb
            """
            function.kinds = kinds
            name = function.__name__
            entry = verbs.get(name) or Verb()
            entry.functions.append(function)
            verbs[name] = entry
            return entry
        return define
    return noun, verb


class Verb:
    """
    An instance of this class stores function definitions associated with a verb.
    :type functions: list
    """
    def __init__(self) -> None:
        self.functions = []

    def __call__(self, *args) -> None:
        """
        :param tuple args: a subject and possibly a complement
        """
        for function in self.functions:
            distribute(function, matches(function, args))


def distribute(function, args, i=0) -> None:
    """
    :param callable function: a function to be invoked, possibly multiple times
    :param list args: constrained arguments wrapped for distribution
    :param int i: the index of the last distributed argument
    """
    if i == len(args):
        return function(*args)
    arg = args[i]
    if arg is None or isinstance(arg, Noun) and not arg.entities:
        arg = [arg]
    for value in arg:
        arguments = list(args)
        arguments[i] = value
        distribute(function, arguments, i=i + 1)


def matches(function, args):
    """
    :param callable function: a function to which args will be distributed
    :param tuple args: unconstrained arguments not wrapped for distribution
    :return: constrained arguments wrapped for distribution
    """
    result = []
    for i, arg in enumerate(args):
        kind = function.kinds[i]
        constrained_arg = compatible(kind, arg)
        if kind.entities:
            result.append([constrained_arg])
        else:
            result.append(constrained_arg)
    return result


def compatible(kind, arg) -> 'Noun':
    """
    :param Noun kind: a noun phrase whose properties constrain the entities
    :param Noun arg: the entities that might be compatible with the kind
    :return: the entities that are compatible with the kind
    """
    entities = arg.entities or [arg]
    for entity in entities:
        for key, value in kind.properties.items():
            if entity.properties[key] != value:
                return None
    return arg


class Noun:
    """
    Subclasses of this class are nouns.
    Instances of this class are noun phrases.
    :type properties: dict
    :type entities: list
    """
    def __init__(self, properties=None, entities=None) -> None:
        """
        :param dict properties: key-value pairs this noun phrase satisfies
        :param list entities: constituents of this noun phrase
        """
        self.properties = properties or {}
        self.entities = entities or []

    def __eq__(self, other) -> bool:
        """
        :param other: any object
        :return: whether self and other have same class and member variables
        """
        return hasattr(other, '__dict__') and self.__dict__ == other.__dict__

    def __iter__(self):
        """
        :return: the constituent entities of the noun phrase
        """
        return iter(self.entities)

    def __getitem__(self, item) -> 'Noun':
        """
        :param int|slice item: the index or indexes to be returned
        :return: a noun with the correct subset of entities
        """
        return Noun(self.properties, self.entities[item])


# # option 1
# exec('function(*args)', {'noun': type('noun', (noun,), {})})
#
# # option 2 -- noun reads from a "frame" dict
# frame = verb.module['frame']
# verb.module['frame'] = {}
# exec(function(*args), globals=verb.module)
# verb.module['frame'] = frame
#
# # option 3 -- noun reads from the bottom and top of a stack of frames
# verb.stack.append({})
# exec(function(*args), locals=verb.stack[-1])
# verb.stack.pop()
#
# # option 4 -- require explicit type conversions
# function(*args)
