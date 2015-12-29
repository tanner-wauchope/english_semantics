
def register() -> tuple:
    """
    :return: a decorator for creating or accessing verbs
             a function for creating or accessing nouns
    """
    nouns = {}

    def noun(name) -> Noun:
        """
        :param str name: the name of the noun to get or create
        :return: the noun that has the name or a new noun
        """
        nouns[name] = nouns.get(name) or type(name, (Noun,), {})
        return nouns[name]()

    verbs = {}

    def verb(function) -> Verb:
        """
        :param callable function: a new definition for a verb
        :return: the verb whose name is the function's name or a new verb
        """
        name = function.__name__
        verbs[name] = verbs.get(name) or Verb()
        verbs[name].functions.append(function)
        return verb

    return noun, verb


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

    def __getitem__(self, item) -> 'Noun':
        """
        :param int|slice item: the index or indexes to be returned
        :return: a noun with the correct subset of entities
        """
        return Noun(self.properties, self.entities[item])


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


def matches(function, args) -> list:
    """
    :param function: a function to which args will be distributed
    :param args: unconstrained arguments not wrapped for distribution
    :return: constrained arguments wrapped for distribution
    """
    result = []
    for key, arg in zip(function.__code__.co_varnames, args):
        kind = function.__annotations__[key]
        entities = compatible(kind, arg.entities)
        if kind.size == 1:
            result.append(entities)
        else:
            result.append([entities])
    return result


def compatible(kind, entities) -> list:
    """
    :param Noun kind: a noun phrase whose properties constrain the entities
    :param list entities: the entities that might be compatible with the kind
    :return: the entities that compatible with the kind
    """
    result = []
    for entity in entities:
        for key, value in kind.properties.items():
            if entity.properties[key] == value:
                result.append(entity)
    return result


def distribute(function, args, i=0) -> None:
    """
    :param callable function: a function to be invoked, possibly multiple times
    :param list args: constrained arguments ready wrapped for distribution
    :param int i: the index of the last distributed argument
    """
    if i == len(args):
        function(*args)
    for value in args[i]:
        arguments = list(args)
        arguments[i] = value
        distribute(function, arguments, i=i + 1)


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