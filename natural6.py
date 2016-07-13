import traceback
import itertools


def is_variable(noun_phrase):
    return isinstance(noun_phrase, str) and not noun_phrase.startswith('"')


def get_value(noun_phrase, scope):
    if is_variable(noun_phrase):
        return scope.get(noun_phrase)
    else:
        return noun_phrase


def get_set(noun_phrase, scope):
    value = get_value(noun_phrase, scope)
    if isinstance(value, set):
        return value
    elif value is None:
        return {}
    else:
        return {value}


class Phrase:
    relations = set()

    def __init__(self, *args):
        self.parts = list(args) or [None]

    def __hash__(self):
        return hash(tuple(id(part) for part in self.parts))

    def __eq__(self, other):
        return type(self) is type(other) and self.parts == other.parts

    def activate(self, scope):
        for i, part in enumerate(self.parts):
            if hasattr(part, 'activate'):
                self.parts[i] = part.activate(scope)
        return self.invoke(scope)

    def invoke(self, scope):
        if self.satisfied(scope):
            return
        elif self.definite(scope):
            cls = type(self)
            for predicate in self.combinations(scope):
                cls.relations.add(predicate)
                subj = predicate.parts[0]
                if hasattr(subj, '__dict__'):
                    predicates = vars(subj).get(cls, [])
                    vars(subj)[cls] = predicates
                    predicates.append(predicate)
        else:
            for part, entity_set in zip(self.parts, self.query(scope)):
                if get_value(part, scope) is None:
                    scope[part] = entity_set

    def query(self, scope):
        predicates = type(self).relations
        for i, part in enumerate(self.parts):
            if get_value(part, scope) is not None:
                result = set()
                for predicate in predicates:
                    if predicate.parts[i] == part:
                        result.add(predicate)
                predicates = result

        for i, part in enumerate(self.parts):
            if get_value(part, scope) is None:
                result = set()
                for predicate in predicates:
                    result.add(predicate.parts[i])
                if len(result) == 0:
                    yield None
                if len(result) == 1:
                    yield result.pop()
                else:
                    yield result
            else:
                yield part

    def combinations(self, scope):
        sets = [get_set(part, scope) for part in self.parts]
        for combination in itertools.product(*sets):
            yield type(self)(*combination)

    def definite(self, scope):
        for part in self.parts:
            if get_value(part, scope) is None:
                return False
        return True

    def satisfied(self, scope):
        if self.definite(scope):
            for relation in self.combinations(scope):
                if relation not in type(self).relations:
                    return False
            return True

        for part, entity_set in zip(self.parts, self.query(scope)):
            if get_value(part, scope) != entity_set:
                return False
        return True


class Expression(Phrase):
    signatures = {
        ((int,), (float,)): (lambda x: None, lambda x: x)
    }


def instantiate(noun, scope):
    if type(noun) is str:
        name = noun.lower()
        cls = type(name.title(), (), {})
    elif hasattr(noun, '__dict__'):
        cls = type(noun)
        name = cls.__name__.lower()
    else:
        raise SyntaxError("Unexpected token after indefinite article")

    entity = cls()
    scope[name] = entity
    return entity


class Instantiation(Expression):
    signatures = (('an', Expression), ('a', Expression),)

    def invoke(self, scope):
        noun = self.parts[1]
        return instantiate(noun, scope)


def lookup(noun, scope):
    if isinstance(noun, str):
        raise NameError
    elif not hasattr(noun, '__dict__'):
        raise TypeError("Unexpected token after 'the'")
    return noun


class Lookup(Expression):
    signatures = (('the', Expression),)

    def invoke(self, scope):
        noun = self.parts[1]
        return lookup(noun, scope)


Expression.signatures.update({
    (('an', Expression), ('a', Expression),): instantiate,
    (('the', Expression),): lookup,
})


class Assignment(Phrase):
    """" Reflexive, transitive, and non-extensible for concrete instances """
    signatures = [(Phrase, 'is', Phrase)]

    def invoke(self, scope):
        subj, verb, obj = self.parts
        if self.satisfied(scope):
            return
        elif is_variable(subj):
            scope[subj] = get_value(obj, scope)
        elif is_variable(obj):
            scope[obj] = get_value(subj, scope)
        else:
            raise ValueError("The arguments cannot be made the same.")

    def satisfied(self, scope):
        subj, verb, obj = self.parts
        return get_value(subj, scope) == get_value(obj, scope)


def split(text, delimiters=' \t\n') -> list:
    """
    :param text: text that may contain the delimiters or quotes
    :param delimiters: tokens to be omitted if unquoted
    :return: the text split by unquoted delimiters, one segment at a time
    """
    text += delimiters
    segment = []
    state = 'unquoted'
    for char in text:
        if state == 'unquoted' and char == '"':
            state = 'quoted'
            segment.append(char)
            continue
        elif state == 'quoted' and char == '"':
            state = 'unquoted'
            segment.append(char)
            continue
        elif state == 'quoted' and char == '\\':
            state = 'escaped'
            continue
        elif state == 'escaped':
            state = 'quoted'
            segment.append(char)
            continue

        if not(char in delimiters and state == 'unquoted'):
            segment.append(char)
        elif segment:
            yield ''.join(segment)
            segment = []

    if state == 'quoted':
        raise SyntaxError('Unclosed quotation: ' + ''.join(segment))


def tokenize(lexemes, scope):
    for lexeme in lexemes:
        try:
            yield eval(lexeme, scope)
        except (NameError, SyntaxError):
            yield scope.get(lexeme, lexeme)


def build_noun_phrases(words, scope):
    # TODO replace with the a more generic implementation
    previous = None
    for i, word in enumerate(words):
        if previous in ('a', 'an'):
            yield Instantiation(previous, word)
        elif previous == 'the':
            yield Lookup(previous, word)
        elif word not in ('a', 'an', 'the'):
            yield word
        previous = word


def parse(primitives, kinds):
    """
    primitives is a list of python instances
    kinds is a sequence of classes
    """
    results = []
    for kind in kinds:
        result = None
        if primitives[0] == kind or isinstance(kind, type) and isinstance(primitives[0], kind):
            result, primitives = primitives[0], primitives[1:]
        elif hasattr(kind, 'signatures'):
            for signature in kind.signatures:
                subresult, remainder = parse(primitives, signature)
                if subresult is not None:
                    result, primitives = kind(*subresult), remainder
                    break
        if result is None:
            return None, None
        results.append(result)
    return results, primitives


def match(phrases, signature):
    if len(phrases) != len(signature):
        return None

    for phrase, kind in zip(phrases, signature):
        is_constant = not isinstance(kind, type) and phrase == kind
        is_variable = isinstance(kind, type) and isinstance(phrase, (str, kind))
        if not (is_constant or is_variable):
            return None
    return signature


def get_signature(phrases, scope):
    result = []
    for phrase in phrases:
        value = get_value(phrase, scope)
        if hasattr(value, '__dict__'):
            result.append(type(value))
        elif value is None:
            result.append(object)
        elif isinstance(value, str):
            result.append(value.strip('"'))
        else:
            result.append(value)
    return result


def unify(phrases, scope):
    for key in scope:
        if hasattr(key, 'signatures'):
            for signature in key.signatures:
                sentence = match(phrases, signature)
                if sentence is not None:
                    return sentence, key
    return None, None


def build_clause(phrases, scope):
    signature, cls = unify(phrases, scope)
    if signature is None:
        signature = get_signature(phrases, scope)
        signatures = [signature]
        cls = type('Sentence', (Phrase,), {'signatures': signatures})
        scope[cls] = signatures
    if len(signature) > 1:
        return cls(*phrases)


def evaluate(line, scope):
    lexemes = split(line)
    tokens = tokenize(lexemes, scope)
    phrases = list(build_noun_phrases(tokens, scope))
    clause = build_clause(phrases, scope)
    if clause:
        clause.activate(scope)
        return ''
    else:
        result = phrases[0]
        if is_variable(result):
            raise NameError(result)
        else:
            return repr(phrases[0]) + '\n'


def interpret():
    scope = {cls: cls.signatures for cls in Phrase.__subclasses__()}
    line = input('> ')
    while line != 'exit':
        try:
            print(evaluate(line, scope), end='')
        except Exception:
            print(traceback.format_exc())
        line = input('> ')


# TODO:
# 1. allow phrases to be defined with indentation
# 2. allow for arbitrary conditions to be attached to functions
#       don't do anything special about inheritance (assume bases are in the "is" predicate
#       run all predicates that match
# 3. add the foreign function interface
# 4. allow prefix trees (useful for all kinds of lists; other kinds of recursive syntax are less important)
# 5. move determiners into the prelude
#       define phrases instead of sentences
#       substructures must match exactly or be variables!
#           this allows recursive syntax to be emulated but discourages unwieldy lines


# import pprint

# class Scope:
#     def __init__(self, stack):
#         self.stack = stack or [{}]
#
#     def __repr__(self):
#         return pprint.pformat(self.stack)
#
#     def __contains__(self, item):
#         for frame in self.stack:
#             if item in frame:
#                 return True
#
#     def __getitem__(self, item):
#         for frame in reversed(self.stack):
#             if item in frame:
#                 return self.stack[-1][item]
#         raise KeyError
#
#     def __setitem__(self, key, value):
#         self.stack[-1][key] = value
#
#     def get(self, item, default=None):
#         if item in self:
#             return self[item]
#         else:
#             return default
